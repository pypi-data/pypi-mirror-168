from typing import TYPE_CHECKING

from ....delivery._data._data_provider import ContentValidator

if TYPE_CHECKING:
    from ....delivery._data._data_provider import ParsedData


class ContentDataValidator(ContentValidator):
    def validate(self, data: "ParsedData") -> bool:
        is_valid = True
        content_data = data.content_data

        counter = 0
        if isinstance(content_data, list):
            for item in content_data:
                if item.get("error"):
                    data.error_codes.append(item["error"]["code"])
                    data.error_messages.append(item["error"]["message"])
                    counter += 1

            if counter == len(content_data):
                is_valid = False

        if content_data is None:
            is_valid = False
            data.error_codes = 1
            data.error_messages = "Content data is None"

        return is_valid
