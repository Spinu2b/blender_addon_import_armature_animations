from typing import Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .....animations_model.model.armature.nodes_hierarchy.node import Node


class NodeInHierarchyInfo:
    def __init__(self, node: 'Node', parent_name: Optional[str]):
        self.node = node  # type: Node
        self.parent_name = parent_name  # type: Optional[str]
