from typing import Any, Tuple

from ...utils.json_parsing.json_parsing_helper import JsonParsingHelper


class JsonDeserializer:
    ATTRIBUTES = {}
    RESULT_CLASS = None

    @classmethod
    def deserialize(cls, json_string: str, parsing_start_char_index: int=0) -> Tuple[Any, int]:
        result = cls.RESULT_CLASS()
        attribute_name, parsing_start_char_index = JsonParsingHelper.get_next_attribute_in_json_object(
            json_string, parsing_start_char_index)
        old_parsing_start_char_index = -1
        while parsing_start_char_index != JsonParsingHelper.INVALID_ATTRIBUTE_CODE:
            python_attribute_name = cls.ATTRIBUTES[attribute_name][0]  # type: str
            deserializer_class = cls.ATTRIBUTES[attribute_name][1]
            parsing_start_char_index = \
                cls._add_attribute(result, python_attribute_name, json_string,
                                   parsing_start_char_index,
                                   deserializer_class)
            old_parsing_start_char_index = parsing_start_char_index
            attribute_name, parsing_start_char_index = JsonParsingHelper.get_next_attribute_in_json_object(
                json_string, parsing_start_char_index)

        return result, old_parsing_start_char_index

    @classmethod
    def _add_attribute(cls, result, python_attribute_name: str,
                       json_string: str, start_char_index: int,
                       deserializer_class) -> int:
        deserialized_object, start_char_index =\
            deserializer_class.deserialize(
                json_string=json_string,
                parsing_start_char_index=start_char_index,
                result_class=deserializer_class.RESULT_CLASS)

        result.__setattr__(object=result, name=python_attribute_name,
                           value=deserialized_object)
        return start_char_index
