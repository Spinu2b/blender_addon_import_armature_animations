from animations_model.model.armature.nodes_hierarchy.nodes_hierarchy import NodesHierarchy
from animations_model.model.blender_poses.blender_consolidated_pose_mode_animation_frame_model import \
    BlenderConsolidatedPoseModeAnimationFrameModel


class FrameModelConsolidator:
    def consolidate(self,
                    unified_armature_model_nodes_hierarchy: NodesHierarchy,
                    animation_frame_model_nodes_hierarchy: NodesHierarchy) ->\
            BlenderConsolidatedPoseModeAnimationFrameModel:
        raise NotImplementedError
