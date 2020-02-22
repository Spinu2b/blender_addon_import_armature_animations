from typing import Tuple, Any

from ...utils.json_parsing.json_parsing_helper import JsonParsingHelper, JsonStringTraversingHelper
from ...utils.json_parsing.json_deserializer import JsonDeserializer


class DictJsonBuildingListener:
    @classmethod
    def on_init(cls):
        raise NotImplementedError

    @classmethod
    def on_key_value_parsing(cls, key: Any, value: Any):
        raise NotImplementedError

    @classmethod
    def get_result(cls) -> Any:
        raise NotImplementedError


class DictJsonDeserializer(JsonDeserializer):
    KEY_JSON_DESERIALIZER_CLASS = None
    VALUE_JSON_DESERIALIZER_CLASS = None
    DICT_BUILDING_RESULT_LISTENER = None

    @classmethod
    def deserialize(cls, json_string: str, parsing_start_char_index: int = 0) -> Tuple[Any, int]:
        result = None

        if cls.DICT_BUILDING_RESULT_LISTENER:
            cls.DICT_BUILDING_RESULT_LISTENER.on_init()
        else:
            result = dict()

        key_value, parsing_start_char_index = JsonParsingHelper.get_next_attribute_in_json_object(
            json_string=json_string,
            parsing_start_char_index=parsing_start_char_index,
            attribute_name_value_deserializer_class=cls.KEY_JSON_DESERIALIZER_CLASS)

        old_parsing_start_char_index = -1
        while parsing_start_char_index != JsonParsingHelper.INVALID_ATTRIBUTE_CODE:
            value_value, parsing_start_char_index = cls.VALUE_JSON_DESERIALIZER_CLASS.deserialize(
                json_string=json_string,
                parsing_start_char_index=parsing_start_char_index
            )

            if cls.DICT_BUILDING_RESULT_LISTENER:
                cls.DICT_BUILDING_RESULT_LISTENER.on_key_value_parsing(key=key_value, value=value_value)
            else:
                result[key_value] = value_value

            old_parsing_start_char_index = parsing_start_char_index
            key_value, parsing_start_char_index = JsonParsingHelper.get_next_attribute_in_json_object(
                json_string=json_string, parsing_start_char_index=parsing_start_char_index,
                attribute_name_value_deserializer_class=cls.KEY_JSON_DESERIALIZER_CLASS)

        old_parsing_start_char_index = JsonParsingHelper.go_to_the_end_of_that_json_object(
            json_string=json_string, parsing_start_char_index=old_parsing_start_char_index)

        if not cls.DICT_BUILDING_RESULT_LISTENER:
            return result, old_parsing_start_char_index
        else:
            return cls.DICT_BUILDING_RESULT_LISTENER.get_result(), old_parsing_start_char_index
