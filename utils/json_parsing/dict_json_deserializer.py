from typing import Tuple, Any

from ...utils.json_parsing.json_parsing_helper import JsonParsingHelper
from ...utils.json_parsing.json_deserializer import JsonDeserializer


class DictJsonDeserializer(JsonDeserializer):
    KEY_JSON_DESERIALIZER_CLASS = None
    VALUE_JSON_DESERIALIZER_CLASS = None

    @classmethod
    def deserialize(cls, json_string: str, parsing_start_char_index: int = 0) -> Tuple[Any, int]:
        result = dict()
        attribute_name, parsing_start_char_index = JsonParsingHelper.get_next_attribute_in_json_object(
            json_string, parsing_start_char_index)
        old_parsing_start_char_index = -1
        while parsing_start_char_index != JsonParsingHelper.INVALID_ATTRIBUTE_CODE:
            key_value, parsing_start_char_index = cls.KEY_JSON_DESERIALIZER_CLASS.deserialize(
                json_string=json_string,
                parsing_start_char_index=parsing_start_char_index
            )
            value_value, parsing_start_char_index = cls.VALUE_JSON_DESERIALIZER_CLASS.deserialize(
                json_string=json_string,
                parsing_start_char_index=parsing_start_char_index
            )
            result[key_value] = value_value
            old_parsing_start_char_index = parsing_start_char_index
            attribute_name, parsing_start_char_index = JsonParsingHelper.get_next_attribute_in_json_object(
                json_string, parsing_start_char_index)

        return result, old_parsing_start_char_index
