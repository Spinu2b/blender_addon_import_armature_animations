import re
from typing import Tuple, Callable


class StringTraversingHelper:
    @classmethod
    def advance_to_next_one_of_these_characters(cls, current_char_index: int,
                                                string_to_search_in: str,
                                                character_criteria: Callable[[str], bool]) -> int:
        current_char_index += 1
        while current_char_index < len(string_to_search_in) and \
                not character_criteria(string_to_search_in[current_char_index]):
            current_char_index += 1

        if current_char_index >= len(string_to_search_in):
            return JsonParsingHelper.INVALID_ATTRIBUTE_CODE
        elif character_criteria(string_to_search_in[current_char_index]):
            return current_char_index
        else:
            raise ValueError('Traversing string went wrong')


class JsonStringTraversingHelper:
    @classmethod
    def advance_from_here_to_attribute_value_opening_char(cls, json_string: str, parsing_start_char_index: int):
        return StringTraversingHelper.advance_to_next_one_of_these_characters(
            current_char_index=parsing_start_char_index,
            string_to_search_in=json_string,
            character_criteria=lambda character: re.match(r"\"|-?[0-9]|{|\[", character) is not None
        )

    @classmethod
    def advance_from_here_to_colon(cls, json_string: str, parsing_start_char_index: int) -> int:
        return StringTraversingHelper.advance_to_next_one_of_these_characters(
            current_char_index=parsing_start_char_index,
            string_to_search_in=json_string,
            character_criteria=lambda character: character == ':'
        )

    @classmethod
    def gather_string_value_and_advance_from_here_to_ending_quote(
            cls, json_string: str, parsing_start_char_index: int) -> Tuple[str, int]:
        end_quote_index = StringTraversingHelper.advance_to_next_one_of_these_characters(
            current_char_index=parsing_start_char_index,
            string_to_search_in=json_string,
            character_criteria=lambda character: character == '"'
        )

        attribute_name = json_string[parsing_start_char_index+1:end_quote_index]
        return attribute_name, end_quote_index

    @classmethod
    def advance_from_here_to_attribute_name_opening_quote(cls, json_string: str, parsing_start_char_index: int) -> int:
        return StringTraversingHelper.advance_to_next_one_of_these_characters(
            current_char_index=parsing_start_char_index,
            string_to_search_in=json_string,
            character_criteria=lambda character: character == '"'
        )

    @classmethod
    def advance_from_here_to_last_digit_of_current_number(cls, json_string: str, parsing_start_char_index: int):
        raise NotImplementedError


class JsonParsingHelper:
    INVALID_CHAR_INDEX = -1
    INVALID_ATTRIBUTE_CODE = -1

    @classmethod
    def get_next_attribute_in_json_object(cls, json_string: str, parsing_start_char_index: int) -> Tuple[str, int]:
        parsing_start_char_index = JsonStringTraversingHelper.advance_from_here_to_attribute_name_opening_quote(
            json_string, parsing_start_char_index)
        attribute_name, parsing_start_char_index = \
            JsonStringTraversingHelper.gather_string_value_and_advance_from_here_to_ending_quote(
                json_string, parsing_start_char_index
            )
        parsing_start_char_index = JsonStringTraversingHelper.advance_from_here_to_colon(
            json_string, parsing_start_char_index)
        parsing_start_char_index = JsonStringTraversingHelper.\
            advance_from_here_to_attribute_value_opening_char(json_string, parsing_start_char_index)
        return attribute_name, parsing_start_char_index

    @classmethod
    def go_to_next_value_in_json_list(cls, json_string: str, parsing_start_char_index: int) -> int:
        raise NotImplementedError

    @classmethod
    def go_to_the_end_of_that_inner_object(cls, json_string: str, parsing_start_char_index: int) -> int:
        raise NotImplementedError
