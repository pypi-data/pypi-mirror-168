import re
from typing import Dict, TYPE_CHECKING

from ._data_grid_type import use_field_names_in_headers_arg_parser
from ..._tools import universe_arg_parser, fields_arg_parser, ADC_TR_PATTERN
from ...delivery._data._data_provider import (
    DataProvider,
    RequestFactory,
    ResponseFactory,
    ContentValidator,
    request_method_value,
    ValidatorContainer,
)
from ...delivery._data._endpoint_data import RequestMethod

if TYPE_CHECKING:
    from ...delivery._data._data_provider import ParsedData

# --------------------------------------------------------------------------------------
#   Response
# --------------------------------------------------------------------------------------
response_errors = {
    "default": "{error_message} Requested universes: {universes}. Requested fields: {"
    "fields}",
    412: "Unable to resolve all requested identifiers in {universes}.",
    218: "Unable to resolve all requested fields in {fields}. The formula must "
    "contain at least one field or function.",
}


class DataGridRDPResponseFactory(ResponseFactory):
    def create_success(self, data: "ParsedData", session: "Session" = None, **kwargs):
        inst = super().create_success(data, **kwargs)
        content_data = data.content_data
        descriptions = content_data.get("messages", {}).get("descriptions", [])
        for descr in descriptions:
            code = descr.get("code")
            if code in {416, 413}:
                inst.errors.append((code, descr.get("description")))
        return inst

    def create_fail(self, data: "ParsedData", universe=None, fields=None, **kwargs):
        error_message = data.first_error_message
        error_code = data.first_error_code
        if error_code not in response_errors.keys():
            data.error_messages = response_errors["default"].format(
                error_message=error_message, fields=fields, universes=universe
            )
        else:
            data.error_messages = response_errors[error_code].format(
                fields=fields, universes=universe
            )

        inst = self.response_class(False, data)
        inst.data = self.data_class(data.content_data)
        inst.data._owner = inst
        return inst


class DataGridUDFResponseFactory(ResponseFactory):
    def get_raw(self, data: "ParsedData"):
        content_data = data.content_data
        return content_data.get("responses", [])[0]

    def create_success(self, data: "ParsedData", session: "Session" = None, **kwargs):
        inst = super().create_success(data, **kwargs)
        raw = self.get_raw(data)
        error = raw.get("error", [])
        for err in error:
            code = err.get("code")
            if code == 416:
                inst.errors.append((code, err.get("message")))

        return inst

    def create_fail(self, data: "ParsedData", universe=None, fields=None, **kwargs):
        error_code = data.first_error_code
        error_message = data.first_error_message

        if error_code not in response_errors.keys():
            data.error_messages = response_errors["default"].format(
                error_message=error_message, fields=fields, universes=universe
            )

        else:
            data.error_messages = response_errors[error_code].format(
                fields=fields, universes=universe
            )

        inst = self.response_class(False, data)
        inst.data = self.data_class(data.content_data)
        inst.data._owner = inst
        return inst


# --------------------------------------------------------------------------------------
#   Request
# --------------------------------------------------------------------------------------


def validate_correct_format_parameters(*_, **kwargs) -> dict:
    parameters = kwargs.get("parameters")
    extended_params = kwargs.get("extended_params")
    universe = kwargs.get("universe")
    fields = kwargs.get("fields")
    use_field_names_in_headers = kwargs.get("use_field_names_in_headers")

    if parameters is not None and not isinstance(parameters, dict):
        raise ValueError(f"Arg parameters must be a dictionary")

    extended_params = extended_params or {}
    universe = extended_params.get("universe") or universe
    universe = universe_arg_parser.get_list(universe)
    universe = [value.upper() if value.islower() else value for value in universe]
    fields = fields_arg_parser.get_list(fields)
    use_field_names_in_headers = use_field_names_in_headers_arg_parser.get_bool(
        use_field_names_in_headers
    )

    kwargs.update(
        {
            "universe": universe,
            "fields": fields,
            "parameters": parameters,
            "use_field_names_in_headers": use_field_names_in_headers,
            "extended_params": extended_params,
        }
    )
    return kwargs


class DataGridRDPRequestFactory(RequestFactory):
    def get_body_parameters(self, *_, **kwargs) -> dict:
        kwargs = validate_correct_format_parameters(*_, **kwargs)
        body_parameters = {}

        universe = kwargs.get("universe")
        if universe:
            body_parameters["universe"] = universe

        fields = kwargs.get("fields")
        if fields:
            body_parameters["fields"] = fields

        parameters = kwargs.get("parameters")
        if parameters:
            body_parameters["parameters"] = parameters

        layout = kwargs.get("layout")
        if isinstance(layout, dict) and layout.get("output"):
            body_parameters["output"] = layout["output"]

        return body_parameters

    def get_request_method(self, **kwargs) -> RequestMethod:
        return RequestMethod.POST


class DataGridUDFRequestFactory(RequestFactory):
    def create(self, session, *args, **kwargs):
        url_root = session._get_rdp_url_root()
        url = url_root.replace("rdp", "udf")

        method = self.get_request_method(**kwargs)
        header_parameters = kwargs.get("header_parameters") or {}
        extended_params = kwargs.get("extended_params") or {}
        body_parameters = self.get_body_parameters(*args, **kwargs)
        body_parameters = self.extend_body_parameters(body_parameters, extended_params)

        headers = {"Content-Type": "application/json"}
        headers.update(header_parameters)
        request = {
            "url": url,
            "method": request_method_value.get(method),
            "headers": headers,
            "body": {
                "Entity": {
                    "E": "DataGrid_StandardAsync",
                    "W": {"requests": [body_parameters]},
                }
            },
        }

        return request

    def get_body_parameters(self, *_, **kwargs) -> dict:

        ticket = kwargs.get("ticket", None)
        if ticket:
            return {"ticket": ticket}

        kwargs = validate_correct_format_parameters(*_, **kwargs)
        body_parameters = {}

        instruments = kwargs.get("universe")
        if instruments:
            body_parameters["instruments"] = instruments

        fields = kwargs.get("fields")
        if fields:
            body_parameters["fields"] = [
                {"name": i} for i in fields if re.match(ADC_TR_PATTERN, i)
            ]

        parameters = kwargs.get("parameters")
        if parameters:
            body_parameters["parameters"] = parameters

        layout = kwargs.get("layout")
        if isinstance(layout, dict) and layout.get("layout"):
            body_parameters["layout"] = layout["layout"]

        return body_parameters

    def get_request_method(self, **kwargs) -> RequestMethod:
        return RequestMethod.POST


# --------------------------------------------------------------------------------------
#   Content data validator
# --------------------------------------------------------------------------------------


class DataGridRDPContentValidator(ContentValidator):
    def validate(self, data: "ParsedData") -> bool:
        is_valid = True

        status = data.status
        status_content = status.get("content", "")

        if status_content.startswith("Failed"):
            is_valid = False
            data.error_codes = -1
            data.error_messages = status_content
            return is_valid

        content_data = data.content_data
        content_data_ = content_data.get("data")
        error = content_data.get("error")

        if not content_data:
            is_valid = False
        elif error and not content_data_:
            is_valid = False
            data.error_codes = error.get("code", -1)
            data.error_messages = error.get("description")

            if not data.error_messages:
                error_message = error.get("message")
                errors = error.get("errors")
                if isinstance(errors, list):
                    error_message += ":\n"
                    error_message += "\n".join(map(str, errors))
                data.error_messages = error_message

        return is_valid


class DataGridUDFContentValidator(ContentValidator):
    def validate(self, data: "ParsedData") -> bool:
        is_valid = True

        status = data.status
        status_content = status.get("content", "")

        if status_content.startswith("Failed"):
            is_valid = False
            data.error_codes = -1
            data.error_messages = status_content
            return is_valid

        content_data = data.content_data
        if isinstance(content_data, str):
            is_valid = False
            data.error_codes = -1
            data.error_messages = content_data
            return is_valid
        elif not content_data:
            is_valid = False
            return is_valid

        response = content_data.get("responses", [])
        response = response[0] if response else {}
        headers = response.get("headers", [])
        headers = headers[0] if headers else {}
        response_data = response.get("data")
        error = response.get("error")

        if not content_data:
            is_valid = False
        elif "ErrorCode" in content_data:
            is_valid = False
            data.error_codes = content_data.get("ErrorCode", -1)
            data.error_messages = content_data.get("ErrorMessage")
        elif error and isinstance(error, dict) and not response_data:
            is_valid = False
            data.error_codes = error.get("code", -1)
            data.error_messages = error.get("message") or error
        elif error and not response_data:
            is_valid = False
            data.error_codes = -1
            data.error_messages = error
        elif headers and error and not all(i.get("displayName") for i in headers):
            is_valid = False
            error_ = error[0]
            data.error_codes = error_.get("code", -1)
            data.error_messages = error_.get("message") or error_

        return is_valid


# --------------------------------------------------------------------------------------
#   Providers
# --------------------------------------------------------------------------------------


data_grid_rdp_data_provider = DataProvider(
    request=DataGridRDPRequestFactory(),
    response=DataGridRDPResponseFactory(),
    validator=ValidatorContainer(content_validator=DataGridRDPContentValidator()),
)

data_grid_udf_data_provider = DataProvider(
    request=DataGridUDFRequestFactory(),
    response=DataGridUDFResponseFactory(),
    validator=ValidatorContainer(content_validator=DataGridUDFContentValidator()),
)
