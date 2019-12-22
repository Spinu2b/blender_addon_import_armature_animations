import copy
from typing import Set

from ....animations_model.model.armature.nodes_hierarchy.nodes_hierarchy import NodesHierarchy, NodeIter
from ....animations_model.model.armature.unified_armature_model import UnifiedArmatureModel
from ....utils.model.tree_hierarchy import TreeNodeInfo


class NodesHierarchiesConsolidator:
    def get_unified_armature_model(self, nodes_hierarchy: NodesHierarchy) -> UnifiedArmatureModel:
        return UnifiedArmatureModel(nodes_hierarchy=nodes_hierarchy)

    def consolidate(self, consolidated_nodes_hierarchy: NodesHierarchy,
                    nodes_hierarchy: NodesHierarchy) -> NodesHierarchy:
        consolidated_nodes_hierarchy = copy.deepcopy(consolidated_nodes_hierarchy)
        consolidated_nodes_hierarchy_nodes_set = set(
            [node_iter.node.name for node_iter in consolidated_nodes_hierarchy.iterate_nodes()])  # type: Set[str]
        nodes_hierarchy_nodes_set = set(
            [node_iter.node.name for node_iter in nodes_hierarchy.iterate_nodes()])  # type: Set[str]
        new_nodes = nodes_hierarchy_nodes_set.difference(consolidated_nodes_hierarchy_nodes_set)
        for new_node_name in new_nodes:
            new_node_info = nodes_hierarchy.get_node(name=new_node_name)  # type: TreeNodeInfo
            consolidated_nodes_hierarchy.add_node(parent_name=new_node_info.parent_name, node=new_node_info.node)
        return consolidated_nodes_hierarchy
