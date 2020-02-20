from typing import Generic, TypeVar

from ...utils.json_parsing.json_deserializer import JsonDeserializer

KeyType = TypeVar('KeyType')
ValueType = TypeVar('ValueType')


class DictJsonDeserializer(JsonDeserializer, Generic[KeyType, ValueType]):
    pass
