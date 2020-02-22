from typing import Tuple

from ...utils.json_parsing.json_deserializer import JsonDeserializer


class BoolJsonDeserializer(JsonDeserializer):
    @classmethod
    def deserialize(cls, json_string: str, parsing_start_char_index: int = 0) -> Tuple[bool, int]:
        bool_value = True if json_string[parsing_start_char_index] == 't' else False
        if bool_value:
            parsing_start_char_index += 3
        else:
            parsing_start_char_index += 4

        return bool_value, parsing_start_char_index
