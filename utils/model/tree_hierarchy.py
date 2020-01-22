import copy
from abc import ABC, abstractmethod
from typing import Optional, List, Iterator


class TreeNodeContainer:
    def __init__(self, node):
        self.children = []  # type: List[TreeNodeContainer]
        self.node = node


class TreeNodeIter:
    def __init__(self, parent, node, children):
        self.parent = parent
        self.node = node
        self.children = children  # type: List[TreeNodeContainer]


class TreeNodeInfo:
    def __init__(self, parent_name: str, node):
        self.parent_name = parent_name  # str
        self.node = node


class TreeNode(ABC):
    @abstractmethod
    def from_json_dict_tree_building(self, json_dict):
        raise NotImplementedError


class TreeHierarchy(ABC):
    def __init__(self):
        self.root = None  # type: Optional[TreeNodeContainer]

    def _traverse_children_recursively_and_put(
            self, parent_name: str, node_to_put: TreeNodeContainer):
        for node_iter in self.iterate_nodes():
            if node_iter.node.name == parent_name:
                node_iter.children.append(node_to_put)
                return
        raise Exception(
            "Did not find parent of that name in tree hierarchy to put node in it: {}".format(parent_name))

    def _traverse_nodes_hierarchy(self, parent: Optional[TreeNodeContainer],
                                  current_node: TreeNodeContainer) -> Iterator[TreeNodeIter]:
        for child_node in current_node.children:
            yield TreeNodeIter(parent=current_node.node,
                               node=child_node.node, children=child_node.children)
        for child_node in current_node.children:
            yield from self._traverse_nodes_hierarchy(parent=current_node, current_node=child_node)

    def add_node(self, parent_name: Optional[str], node):
        node = copy.deepcopy(node)
        node_container = TreeNodeContainer(node=node)
        if parent_name is None:
            self.root = node_container
        else:
            self._traverse_children_recursively_and_put(
                parent_name=parent_name,
                node_to_put=node_container)

    def iterate_nodes(self) -> Iterator[TreeNodeIter]:
        if self.root is not None:
            yield TreeNodeIter(parent=None,
                               node=self.root.node, children=self.root.children)
            yield from self._traverse_nodes_hierarchy(parent=None, current_node=self.root)

    def get_node(self, name: str) -> TreeNodeInfo:
        for node_iter in self.iterate_nodes():
            if node_iter.node.name == name:
                node = copy.deepcopy(node_iter.node)
                return TreeNodeInfo(parent_name=node_iter.parent.name if node_iter.parent is not None else None,
                                    node=node)
        raise Exception("Did not find node of that name in tree hierarchy: {}".format(name))

    def get_root(self) -> TreeNodeContainer:
        return self.root
