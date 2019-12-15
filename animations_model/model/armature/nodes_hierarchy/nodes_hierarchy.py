import copy
from typing import Optional, Generator

from animations_model.model.armature.nodes_hierarchy.node import Node


class NodeIter:
    def __init__(self, parent: Node, node: Node):
        self.parent = parent  # type: Optional[Node]
        self.node = node  # type: Node


class NodeInfo:
    def __init__(self, parent_name: str, node: Node):
        self.parent_name = parent_name  # type: Optional[str]
        self.node = node  # type: Node


class NodesHierarchy:
    def __init__(self):
        self.root = None  # type: Optional[Node]

    def _traverse_children_recursively_and_put(
            self, parent_name: str, node_to_put: Node):
        for node_iter in self.iterate_nodes():
            if node_iter.node.name == parent_name:
                node_iter.node.children.append(node_to_put)
                return
        raise Exception(
            "Did not find parent of that name in nodes hierarchy to put node in it: {}".format(parent_name))

    def _traverse_nodes_hierarchy(self, parent: Optional[Node], current_node: Node) -> Generator[NodeIter]:
        yield NodeIter(parent=parent, node=current_node)
        for child_node in current_node.children:
            yield from self._traverse_nodes_hierarchy(parent=current_node, current_node=child_node)

    def add_node(self, parent_name: Optional[str], node: Node):
        node = copy.deepcopy(node)
        node.children = []
        if parent_name is None:
            self.root = node
        else:
            self._traverse_children_recursively_and_put(
                parent_name=parent_name,
                node_to_put=node)

    def iterate_nodes(self) -> Generator[NodeIter]:
        yield from self._traverse_nodes_hierarchy(parent=None, current_node=self.root)

    def get_node(self, name: str) -> NodeInfo:
        for node_iter in self.iterate_nodes():
            if node_iter.node.name == name:
                node = copy.deepcopy(node_iter.node)
                node.children = []
                return NodeInfo(parent_name=node_iter.parent.name if node_iter.parent is not None else None,
                                node=node)
        raise Exception("Did not find node of that name in nodes hierarchy: {}".format(name))
