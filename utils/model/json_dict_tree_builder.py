from typing import Type

from utils.model.tree_hierarchy import TreeHierarchy


class JsonDictTreeBuilder:
    def build_from(self, tree_class: Type[TreeHierarchy], tree_node_class, animation_frame_dict) -> TreeHierarchy:
        raise NotImplementedError
