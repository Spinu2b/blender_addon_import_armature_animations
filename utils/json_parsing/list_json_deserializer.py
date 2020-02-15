from typing import Generic, TypeVar

from utils.json_parsing.json_deserializer import JsonDeserializer

T = TypeVar('T')


class ListJsonDeserializer(JsonDeserializer, Generic[T]):
    pass
