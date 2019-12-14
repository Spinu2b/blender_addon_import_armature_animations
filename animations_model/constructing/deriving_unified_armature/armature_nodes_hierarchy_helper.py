from animations_model.constructing.deriving_unified_armature.nodes_hierarchies_consolidator import \
    NodesHierarchiesConsolidator
from animations_model.model.armature.nodes_hierarchy.nodes_hierarchy import NodesHierarchy


class ArmatureNodesHierarchyHelper:
    def derive_nodes_hierarchy_from_animation_clip(self, animation_clip):
        animation_frame_model = animation_clip.get_first_animation_frame()
        return animation_frame_model.get_nodes_hierarchy()

    def derive_most_comprehensive_armature_model_from_nodes_hierarchies(self, nodes_hierarchies):
        nodes_hierarchies_consolidator = NodesHierarchiesConsolidator()
        consolidated_nodes_hierarchy = NodesHierarchy()
        for nodes_hierarchy in nodes_hierarchies:
            consolidated_nodes_hierarchy = nodes_hierarchies_consolidator.\
                consolidate(consolidated_nodes_hierarchy, nodes_hierarchy)
        return nodes_hierarchies_consolidator.get_unified_armature_model(consolidated_nodes_hierarchy)
