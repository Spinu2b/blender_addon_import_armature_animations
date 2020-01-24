from typing import Type, List, Tuple, Optional

from ...utils.model.tree_hierarchy import TreeHierarchy


class JsonDictTreeBuilder:
    def build_from(self, tree_class: Type[TreeHierarchy], tree_node_class,
                   json_dict_tree) -> TreeHierarchy:
        result = tree_class()  # type: TreeHierarchy
        self._traverse_and_build_tree(
            tree=result,
            tree_node_class=tree_node_class,
            parent_key=None,
            node_key=json_dict_tree["Root"]["Id"],
            current_json_dict_tree_node=json_dict_tree["Root"])
        return result

    def _traverse_and_build_tree(
            self,
            tree: TreeHierarchy,
            tree_node_class,
            parent_key,
            node_key,
            current_json_dict_tree_node):
        current_node = tree_node_class.from_json_dict_tree_building(current_json_dict_tree_node["Node"])
        tree.add_node(
            parent_key=parent_key,
            node_key=node_key,
            node=current_node
        )
        for current_node_child_json_dict in current_json_dict_tree_node["Children"]:
            self._traverse_and_build_tree(
                tree=tree,
                tree_node_class=tree_node_class,
                parent_key=node_key,
                node_key=current_node_child_json_dict["Id"],
                current_json_dict_tree_node=current_node_child_json_dict
            )
