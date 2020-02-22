from typing import Tuple

from ...utils.json_parsing.json_parsing_helper import JsonStringTraversingHelper
from ...utils.json_parsing.json_deserializer import JsonDeserializer


class FloatJsonDeserializer(JsonDeserializer):
    @classmethod
    def deserialize(cls, json_string: str, parsing_start_char_index: int = 0) -> Tuple[float, int]:
        last_digit_index = JsonStringTraversingHelper.advance_from_here_to_last_digit_of_current_number(
            json_string, parsing_start_char_index
        )
        number_value = json_string[parsing_start_char_index:last_digit_index + 1]
        number_value = number_value.replace('"', '')
        float_value = float(number_value)
        return float_value, last_digit_index
