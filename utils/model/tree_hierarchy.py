import copy
from abc import ABC
from typing import Optional, List, Iterator, TypeVar, Generic

KeyType = TypeVar("KeyType")
NodeType = TypeVar("NodeType")


class TreeNodeContainer(Generic[KeyType, NodeType]):
    def __init__(self, key: KeyType, node: NodeType):
        self.children = []  # type: List[TreeNodeContainer[KeyType, NodeType]]
        self.key = key  # type: KeyType
        self.node = node  # type: NodeType


class TreeNodeIter(Generic[KeyType, NodeType]):
    def __init__(self, parent: NodeType, node: NodeType, parent_key: KeyType, key: KeyType,
                 children: List[TreeNodeContainer[KeyType, NodeType]]):
        self.parent = parent  # type: NodeType
        self.node = node  # type: NodeType
        self.parent_key = parent_key  # type: KeyType
        self.key = key  # type: KeyType
        self.children = children  # type: List[TreeNodeContainer[KeyType, NodeType]]


class TreeNodeInfo(Generic[KeyType, NodeType]):
    def __init__(self, parent_key: KeyType, node: NodeType):
        self.parent_key = parent_key  # type: KeyType
        self.node = node  # type: NodeType


class TreeHierarchy(ABC, Generic[KeyType, NodeType]):
    def __init__(self):
        self.root = None  # type: Optional[TreeNodeContainer[KeyType, NodeType]]

    def _traverse_children_recursively_and_put(
            self, parent_key: KeyType, node_to_put: TreeNodeContainer[KeyType, NodeType]):
        for node_iter in self.iterate_nodes():
            if node_iter.key == parent_key:
                node_iter.children.append(node_to_put)
                return
        raise Exception(
            "Did not find parent of that key in tree hierarchy to put node in it: {}".format(parent_key))

    def _traverse_nodes_hierarchy(self, parent: Optional[TreeNodeContainer[KeyType, NodeType]],
                                  current_node: TreeNodeContainer[KeyType, NodeType]) -> \
            Iterator[TreeNodeIter[KeyType, NodeType]]:
        for child_node in current_node.children:
            yield TreeNodeIter(parent=current_node.node,
                               node=child_node.node,
                               parent_key=current_node.key,
                               key=child_node.key,
                               children=child_node.children)
        for child_node in current_node.children:
            yield from self._traverse_nodes_hierarchy(parent=current_node, current_node=child_node)

    def add_node(self, parent_key: KeyType, node_key: KeyType, node: NodeType):
        node = copy.deepcopy(node)
        node_container = TreeNodeContainer(node=node, key=node_key)
        if parent_key is None:
            if self.root is not None:
                raise ValueError("Tree already contains root node!")
            self.root = node_container
        else:
            self._traverse_children_recursively_and_put(
                parent_key=parent_key,
                node_to_put=node_container)

    def iterate_nodes(self) -> Iterator[TreeNodeIter[KeyType, NodeType]]:
        if self.root is not None:
            yield TreeNodeIter(parent=None,
                               node=self.root.node,
                               parent_key=None,
                               key=self.root.key,
                               children=self.root.children)
            yield from self._traverse_nodes_hierarchy(parent=None, current_node=self.root)

    def iterate_parent_child_key_pairs(self):
        for node_iter in self.iterate_nodes():
            yield (node_iter.parent_key, node_iter.key)

    def get_node(self, key) -> TreeNodeInfo[KeyType, NodeType]:
        for node_iter in self.iterate_nodes():
            if node_iter.key == key:
                node = copy.deepcopy(node_iter.node)
                return TreeNodeInfo(parent_key=node_iter.parent_key if node_iter.parent is not None else None,
                                    node=node)
        raise Exception("Did not find node of that key in tree hierarchy: {}".format(key))

    def get_root(self) -> TreeNodeContainer[KeyType, NodeType]:
        return self.root
