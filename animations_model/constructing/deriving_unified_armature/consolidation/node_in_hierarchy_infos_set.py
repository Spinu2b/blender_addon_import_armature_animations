import copy
from functools import cmp_to_key
from typing import Set, List
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .....animations_model.constructing.deriving_unified_armature.consolidation.node_in_hierarchy_info import \
        NodeInHierarchyInfo
    from .....animations_model.model.armature.nodes_hierarchy.nodes_hierarchy import NodesHierarchy


class SortingNodesInHierarchyInfosInPuttingOrder:
    @classmethod
    def compare(cls,
                node_in_hierarchy_info_a: 'NodeInHierarchyInfo',
                node_in_hierarchy_info_b: 'NodeInHierarchyInfo') -> int:
        if node_in_hierarchy_info_a.node.name == node_in_hierarchy_info_b.parent_name:
            return -1
        elif node_in_hierarchy_info_b.node.name == node_in_hierarchy_info_a.parent_name:
            return 1
        else:
            return 0


class NodeInHierarchyInfosSet:
    def __init__(self, node_in_hierarchy_infos_set: Set['NodeInHierarchyInfo']):
        self.node_in_hierarchy_infos_set = node_in_hierarchy_infos_set  # type: Set[NodeInHierarchyInfo]

    def difference(self, another):
        return NodeInHierarchyInfosSet(
            node_in_hierarchy_infos_set=
            self.node_in_hierarchy_infos_set.difference(another.node_in_hierarchy_infos_set))

    def _sort_in_putting_order(self, nodes_in_hierarchy_infos_list: List['NodeInHierarchyInfo']) \
            -> List['NodeInHierarchyInfo']:
        nodes_in_hierarchy_infos_list = copy.deepcopy(nodes_in_hierarchy_infos_list)
        return sorted(nodes_in_hierarchy_infos_list,
                      key=cmp_to_key(SortingNodesInHierarchyInfosInPuttingOrder.compare))

    def fullfil_nodes_hierarchy_with_parent_child_chains(self, nodes_hierarchy: 'NodesHierarchy') -> 'NodesHierarchy':
        nodes_hierarchy = copy.deepcopy(nodes_hierarchy)
        for node_info in self._sort_in_putting_order(list(self.node_in_hierarchy_infos_set)):
            if node_info.node.name not in nodes_hierarchy.get_nodes_names():
                nodes_hierarchy.add_node(parent_name=node_info.parent_name, node=node_info.node)
        return nodes_hierarchy
