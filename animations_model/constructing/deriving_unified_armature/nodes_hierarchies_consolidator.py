from animations_model.constructing.deriving_unified_armature.nodes_hierarchy_to_unified_armature_model_converter import \
    NodesHierarchyToUnifiedArmatureModelConverter


class NodesHierarchiesConsolidator:
    def get_unified_armature_model(self, nodes_hierarchy):
        return NodesHierarchyToUnifiedArmatureModelConverter().convert(nodes_hierarchy)

    def consolidate(self, consolidated_nodes_hierarchy, nodes_hierarchy):
        pass
