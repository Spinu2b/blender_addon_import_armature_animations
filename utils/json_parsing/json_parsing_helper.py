import re
from typing import Tuple, Callable, Any


class StringTraversingHelper:
    @classmethod
    def advance_to_next_one_of_these_characters(cls, current_char_index: int,
                                                string_to_search_in: str,
                                                character_criteria: Callable[[str], bool]) -> int:
        print("Char: {}/{}".format(current_char_index, len(string_to_search_in)))

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
    def advance_from_here_to_attribute_value_opening_char(cls, json_string: str, parsing_start_char_index: int) -> int:
        return StringTraversingHelper.advance_to_next_one_of_these_characters(
            current_char_index=parsing_start_char_index,
            string_to_search_in=json_string,
            character_criteria=lambda character: re.match(r"\"|-?[0-9]|{|\[|t|f", character) is not None
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
    def advance_from_here_to_last_digit_of_current_number(cls, json_string: str, parsing_start_char_index: int) -> int:
        return StringTraversingHelper.advance_to_next_one_of_these_characters(
            current_char_index=parsing_start_char_index,
            string_to_search_in=json_string,
            character_criteria=lambda character: re.match(r"[^-0-9.]", character) is not None
        ) - 1

    @classmethod
    def signal_invalid_attribute_code_if_encounter_end_of_object(cls, json_string: str, parsing_start_char_index: int)\
            -> int:
        parsing_start_char_index += 1
        while json_string[parsing_start_char_index] not in ['}', ']']:
            if json_string[parsing_start_char_index] == '"':  # we encounter more attributes to parse in current object
                return JsonParsingHelper.VALID_FURTHER_ATTRIBUTES
            parsing_start_char_index += 1
        return JsonParsingHelper.INVALID_ATTRIBUTE_CODE

    @classmethod
    def advance_from_here_to_end_of_json_object(cls, json_string: str, parsing_start_char_index: int) -> int:
        return StringTraversingHelper.advance_to_next_one_of_these_characters(
            current_char_index=parsing_start_char_index,
            string_to_search_in=json_string,
            character_criteria=lambda character: character in [']', '}']
        )


class JsonParsingHelper:
    VALID_FURTHER_ATTRIBUTES = 1
    INVALID_CHAR_INDEX = -1
    INVALID_ATTRIBUTE_CODE = -1

    @classmethod
    def get_next_attribute_in_json_object(cls, json_string: str, parsing_start_char_index: int,
                                          attribute_name_value_deserializer_class: Any) \
            -> Tuple[Any, int]:
        attribute_mark = JsonStringTraversingHelper.signal_invalid_attribute_code_if_encounter_end_of_object(
            json_string, parsing_start_char_index
        )
        if attribute_mark == cls.INVALID_ATTRIBUTE_CODE:
            return "", cls.INVALID_ATTRIBUTE_CODE

        parsing_start_char_index = JsonStringTraversingHelper.advance_from_here_to_attribute_name_opening_quote(
            json_string, parsing_start_char_index)
        attribute_name_value, parsing_start_char_index = attribute_name_value_deserializer_class.deserialize(
            json_string=json_string,
            parsing_start_char_index=parsing_start_char_index
        )

        #attribute_name, parsing_start_char_index = \
        #    JsonStringTraversingHelper.gather_string_value_and_advance_from_here_to_ending_quote(
        #        json_string, parsing_start_char_index
        #    )

        parsing_start_char_index = JsonStringTraversingHelper.advance_from_here_to_colon(
            json_string, parsing_start_char_index)
        parsing_start_char_index = JsonStringTraversingHelper.\
            advance_from_here_to_attribute_value_opening_char(json_string, parsing_start_char_index)
        return attribute_name_value, parsing_start_char_index

    @classmethod
    def go_to_next_value_in_json_list(cls, json_string: str, parsing_start_char_index: int) -> int:
        list_value_mark = JsonStringTraversingHelper.signal_invalid_attribute_code_if_encounter_end_of_object(
            json_string, parsing_start_char_index
        )

        if list_value_mark == cls.INVALID_ATTRIBUTE_CODE:
            return cls.INVALID_ATTRIBUTE_CODE

        parsing_start_char_index = JsonStringTraversingHelper. \
            advance_from_here_to_attribute_value_opening_char(json_string, parsing_start_char_index)
        return parsing_start_char_index

    @classmethod
    def go_to_the_end_of_that_json_object(cls, json_string: str, parsing_start_char_index: int) -> int:
        return JsonStringTraversingHelper.advance_from_here_to_end_of_json_object(json_string, parsing_start_char_index)
