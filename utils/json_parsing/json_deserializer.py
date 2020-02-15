from typing import Any

from utils.json_parsing.json_parsing_helper import JsonParsingHelper


class JsonDeserializer:
    ATTRIBUTES = {}
    RESULT_CLASS = None

    @classmethod
    def deserialize(cls, json_string: str, parsing_start_char_index: int, result_class: Any):
        result = result_class()
        for attribute_name, attribute_value_str_start_char_index in JsonParsingHelper.iterate_object_attributes(
                json_string, parsing_start_char_index):
            python_attribute_name = cls.ATTRIBUTES[attribute_name][0]  # type: str
            deserializer_class = cls.ATTRIBUTES[attribute_name][1]
            cls.add_attribute(result, python_attribute_name, json_string, attribute_value_str_start_char_index,
                              deserializer_class)

        return result

    @classmethod
    def add_attribute(cls, result, python_attribute_name: str,
                      json_string: str, start_char_index: int,
                      deserializer_class):
        result.__setattr__(object=result, name=python_attribute_name,
                           value=deserializer_class.deserialize(
                               json_string=json_string,
                               parsing_start_char_index=start_char_index,
                               result_class=deserializer_class.RESULT_CLASS))
