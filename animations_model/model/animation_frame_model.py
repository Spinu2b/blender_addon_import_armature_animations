from animations_model.constructing.deriving_unified_armature.animation_frame_model_to_nodes_hierarchy_converter import \
    AnimationFrameModelToNodesHierarchyConverter


class AnimationFrameModel:
    def __init__(self):
        self.nodes = []

    def get_nodes_hierarchy(self):
        return AnimationFrameModelToNodesHierarchyConverter().convert(self)
