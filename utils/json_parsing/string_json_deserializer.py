from typing import Tuple

from ...utils.json_parsing.json_parsing_helper import JsonStringTraversingHelper
from ...utils.json_parsing.json_deserializer import JsonDeserializer


class StringJsonDeserializer(JsonDeserializer):
    @classmethod
    def deserialize(cls, json_string: str, parsing_start_char_index: int = 0) -> Tuple[str, int]:
        str_value, last_digit_index = JsonStringTraversingHelper.\
            gather_string_value_and_advance_from_here_to_ending_quote(
                json_string, parsing_start_char_index
            )
        return str_value, last_digit_index
