from typing import Generic, TypeVar

from utils.json_parsing.json_deserializer import JsonDeserializer

TreeSubclass = TypeVar('TreeSubclass')
TreeNodeKeyJsonDeserializerClass = TypeVar('TreeNodeKeyJsonDeserializerClass')
TreeNodeJsonDeserializerClass = TypeVar('TreeNodeJsonDeserializerClass')


class TreeJsonDeserializer(JsonDeserializer, Generic[TreeSubclass, TreeNodeKeyJsonDeserializerClass,
                                                     TreeNodeJsonDeserializerClass]):
    pass
