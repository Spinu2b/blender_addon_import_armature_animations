import copy
from typing import Set
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .....animations_model.constructing.deriving_unified_armature.consolidation.node_in_hierarchy_info import \
        NodeInHierarchyInfo
    from .....animations_model.model.armature.nodes_hierarchy.nodes_hierarchy import NodesHierarchy


class NodeInHierarchyInfosSet:
    def __init__(self, node_in_hierarchy_infos_set: Set['NodeInHierarchyInfo']):
        self.node_in_hierarchy_infos_set = node_in_hierarchy_infos_set  # type: Set[NodeInHierarchyInfo]

    def difference(self, another):
        return NodeInHierarchyInfosSet(
            node_in_hierarchy_infos_set=
            self.node_in_hierarchy_infos_set.difference(another.node_in_hierarchy_infos_set))

    def fullfil_nodes_hierarchy_with_parent_child_chains(self, nodes_hierarchy: 'NodesHierarchy') -> 'NodesHierarchy':
        nodes_hierarchy = copy.deepcopy(nodes_hierarchy)
        node_in_hierarchy_info_set = copy.deepcopy(self.node_in_hierarchy_infos_set)
        while len(node_in_hierarchy_info_set) > 0:
            node_info = node_in_hierarchy_info_set.pop()
            if node_info.node.name not in nodes_hierarchy.get_nodes_names() \
                    and (node_info.parent_name is None or node_info.parent_name in nodes_hierarchy.get_nodes_names()):
                nodes_hierarchy.add_node(parent_name=node_info.parent_name, node=node_info.node)

            if node_info.node.name not in nodes_hierarchy.get_nodes_names():
                node_in_hierarchy_info_set.add(node_info)

        return nodes_hierarchy
