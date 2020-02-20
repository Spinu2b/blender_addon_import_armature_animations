from typing import Tuple, Any

from ...utils.json_parsing.json_deserializer import JsonDeserializer
from ...utils.json_parsing.json_parsing_helper import JsonParsingHelper


class ListJsonDeserializer(JsonDeserializer):
    LIST_ELEMENT_JSON_DESERIALIZER_CLASS = None

    @classmethod
    def deserialize(cls, json_string: str, parsing_start_char_index: int = 0) -> Tuple[Any, int]:
        result = []
        attribute_name, parsing_start_char_index = JsonParsingHelper.go_to_next_value_in_json_list(
            json_string, parsing_start_char_index)
        old_parsing_start_char_index = -1
        while parsing_start_char_index != JsonParsingHelper.INVALID_ATTRIBUTE_CODE:
            element_obj, parsing_start_char_index = cls.LIST_ELEMENT_JSON_DESERIALIZER_CLASS.deserialize(
                json_string=json_string,
                parsing_start_char_index=parsing_start_char_index
            )
            result.append(element_obj)
            old_parsing_start_char_index = parsing_start_char_index
            attribute_name, parsing_start_char_index = JsonParsingHelper.go_to_next_value_in_json_list(
                json_string, parsing_start_char_index)

        old_parsing_start_char_index = JsonParsingHelper.go_to_the_end_of_that_json_object(
            json_string=json_string, parsing_start_char_index=old_parsing_start_char_index)

        return result, old_parsing_start_char_index
