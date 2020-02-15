from typing import Generic, TypeVar

KeyType = TypeVar('KeyType')
ValueType = TypeVar('ValueType')


class DictJsonDeserializer(Generic[KeyType, ValueType]):
    @classmethod
    def deserialize(cls, json_string: str, parsing_start_char_index: int):
        raise NotImplementedError
