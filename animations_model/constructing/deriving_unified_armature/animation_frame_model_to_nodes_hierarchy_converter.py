from animations_model.model.animations.animation_frame_model import AnimationFrameModel
from animations_model.model.armature.nodes_hierarchy.nodes_hierarchy import NodesHierarchy


class AnimationFrameModelToNodesHierarchyConverter:
    def convert(self, animation_frame_model: AnimationFrameModel) -> NodesHierarchy:
        result = NodesHierarchy()
        for animation_frame_node_iter in animation_frame_model.iterate_nodes():
            result.add_node(
                animation_frame_node_iter.parent.node_name if animation_frame_node_iter.parent is not None else None,
                animation_frame_node_iter.animation_frame_node_model)
        return result
