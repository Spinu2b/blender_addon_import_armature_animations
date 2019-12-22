from animations_model.model.animations.animation_frame_model import AnimationFrameModel
from animations_model.model.armature.blender.blender_edit_mode_armature_model import BlenderEditModeArmatureModel
from animations_model.model.armature.unified_armature_model import UnifiedArmatureModel
from animations_model.model.blender_poses.blender_consolidated_pose_mode_animation_frame_model import \
    BlenderConsolidatedPoseModeAnimationFrameModel
from blender_api.blender_operations.constructing_animations.deriving_pose.frame_model_consolidator import \
    FrameModelConsolidator
from utils.model_spaces_integration.model_spaces_info import ModelSpacesInfo


class AnimationFrameModelToBlenderPoseModeAnimationFrameModelConverter:
    def derive_using_consolidation_of_armature_models_with_home_positioning(
            self,
            unified_armature_model: UnifiedArmatureModel,
            blender_edit_mode_armature_model: BlenderEditModeArmatureModel,
            animation_frame_model: AnimationFrameModel) -> BlenderConsolidatedPoseModeAnimationFrameModel:
        unified_armature_model = unified_armature_model.translate_to_space_model(
            base_space_model=ModelSpacesInfo.MODEL_AXIS_INFO,
            target_space_model=ModelSpacesInfo.BLENDER_AXIS_INFO
        )

        animation_frame_model_nodes_hierarchy = animation_frame_model.get_nodes_hierarchy().translate_to_space_model(
            base_space_model=ModelSpacesInfo.MODEL_AXIS_INFO,
            target_space_model=ModelSpacesInfo.BLENDER_AXIS_INFO
        )

        blender_consolidated_pose_mode_animation_frame_model = FrameModelConsolidator() \
            .consolidate(
                unified_armature_model_nodes_hierarchy=unified_armature_model.nodes_hierarchy,
                animation_frame_model_nodes_hierarchy=animation_frame_model_nodes_hierarchy
            )
        return blender_consolidated_pose_mode_animation_frame_model
