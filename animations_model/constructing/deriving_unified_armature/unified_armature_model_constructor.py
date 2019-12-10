from animations_model.constructing.deriving_unified_armature.armature_nodes_hierarchy_helper import \
    ArmatureNodesHierarchyHelper


class UnifiedArmatureModelConstructor:
    def derive_unified_armature_model_from_animation_clips(self, animation_clips):
        nodes_hierarchies = []
        armature_nodes_hierarchy_helper = ArmatureNodesHierarchyHelper()
        for animation_clip in animation_clips:
            nodes_hierarchy = armature_nodes_hierarchy_helper.derive_nodes_hierarchy_from_animation_clip(animation_clip)
            nodes_hierarchies.append(nodes_hierarchy)
        unified_armature_model = armature_nodes_hierarchy_helper.\
            derive_most_comprehensive_armature_model_from_nodes_hierarchies(nodes_hierarchies)
        return unified_armature_model
