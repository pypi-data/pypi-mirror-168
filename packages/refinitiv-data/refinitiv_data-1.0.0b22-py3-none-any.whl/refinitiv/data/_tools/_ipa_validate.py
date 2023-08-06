from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from refinitiv.data.delivery._data._data_provider import ParsedData


def do_all_elements_have_error(data: "ParsedData", elements: list) -> bool:
    counter = len(elements) or 1
    for element in elements:

        if not hasattr(element, "get"):
            counter -= 1
            data.error_messages = f"Invalid data type={type(element)}, data={element}"
            continue

        error = element.get("error")

        if error:
            counter -= 1
            error_code = error.get("code")
            data.error_codes.append(error_code)
            error_message = error.get("message")
            data.error_messages.append(error_message)

    if counter == 0:
        return True

    return False
