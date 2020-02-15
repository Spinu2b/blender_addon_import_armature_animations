from typing import Iterator, Tuple


class JsonStringTraversingHelper:
    @classmethod
    def get_next_attribute_info(cls, json_string: str, current_char_index: int) -> Tuple[str, int]:
        current_char_index = cls._advance_from_here_to_attribute_name_opening_quote(json_string, current_char_index)
        attribute_name, current_char_index = cls._harvest_attribute_name_and_advance_to_colon(
            json_string, current_char_index)
        current_char_index = cls._advance_from_here_to_char_beginning_attribute_actual_value_definition(
            json_string, current_char_index)

    @classmethod
    def _advance_from_here_to_attribute_name_opening_quote(cls, json_string: str, current_char_index: int) -> int:
        raise NotImplementedError

    @classmethod
    def _harvest_attribute_name_and_advance_to_colon(cls, json_string: str, current_char_index: int) -> int:
        raise NotImplementedError

    @classmethod
    def _advance_from_here_to_char_beginning_attribute_actual_value_definition(
            cls, json_string: str, current_char_index: int) -> int:
        raise NotImplementedError


class JsonParsingHelper:
    @classmethod
    def iterate_object_attributes(cls, json_string: str, parsing_start_char_index: int) -> Iterator[Tuple[str, int]]:
        attribute_value_start_char_index = parsing_start_char_index + 1
        attribute_name, attribute_value_start_char_index = \
            JsonStringTraversingHelper.get_next_attribute_info(json_string, attribute_value_start_char_index)
        while attribute_value_start_char_index != -1:
            yield attribute_name, attribute_value_start_char_index
            attribute_name, attribute_value_start_char_index = \
                JsonStringTraversingHelper.get_next_attribute_info(json_string, attribute_value_start_char_index)
