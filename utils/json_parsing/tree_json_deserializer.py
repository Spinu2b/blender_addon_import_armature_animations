from typing import Generic, TypeVar

TreeSubclass = TypeVar('TreeSubclass')
TreeNodeClass = TypeVar('TreeNodeClass')


class TreeJsonDeserializer(Generic[TreeSubclass, TreeNodeClass]):
    pass
