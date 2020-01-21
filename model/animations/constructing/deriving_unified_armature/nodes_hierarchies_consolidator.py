import copy
from typing import TYPE_CHECKING

from ....animations_model.constructing.deriving_unified_armature.consolidation.node_in_hierarchy_infos_set import \
    NodeInHierarchyInfosSet
from ....animations_model.constructing.deriving_unified_armature.consolidation.node_in_hierarchy_info import \
    NodeInHierarchyInfo
from ....animations_model.model.armature.unified_armature_model import UnifiedArmatureModel

if TYPE_CHECKING:
    from ....animations_model.model.armature.nodes_hierarchy.nodes_hierarchy import NodesHierarchy


class NodesHierarchiesConsolidator:
    def get_unified_armature_model(self, nodes_hierarchy: 'NodesHierarchy') -> UnifiedArmatureModel:
        return UnifiedArmatureModel(nodes_hierarchy=nodes_hierarchy)

    def consolidate(self, consolidated_nodes_hierarchy: 'NodesHierarchy',
                    nodes_hierarchy: 'NodesHierarchy') -> 'NodesHierarchy':
        consolidated_nodes_hierarchy = copy.deepcopy(consolidated_nodes_hierarchy)
        consolidated_nodes_hierarchy_nodes_set = \
            NodeInHierarchyInfosSet(
                set([NodeInHierarchyInfo(parent_name=node_iter.parent.name if node_iter.parent is not None else None,
                                         node=node_iter.node)
                    for node_iter in consolidated_nodes_hierarchy.iterate_nodes()]))
        nodes_hierarchy_nodes_set = \
            NodeInHierarchyInfosSet(
                set([NodeInHierarchyInfo(parent_name=node_iter.parent.name if node_iter.parent is not None else None,
                                         node=node_iter.node)
                    for node_iter in nodes_hierarchy.iterate_nodes()]))
        new_nodes = nodes_hierarchy_nodes_set.difference(consolidated_nodes_hierarchy_nodes_set)
        consolidated_nodes_hierarchy = new_nodes.\
            fullfil_nodes_hierarchy_with_parent_child_chains(consolidated_nodes_hierarchy)
        return consolidated_nodes_hierarchy
