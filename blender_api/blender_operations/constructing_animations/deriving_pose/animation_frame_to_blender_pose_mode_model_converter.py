from typing import TYPE_CHECKING, Tuple

from .....blender_api.blender_operations.constructing_animations.deriving_pose.frame_model_consolidator import \
    FrameModelConsolidator
from .....utils.model_spaces_integration.model_spaces_info import ModelSpacesInfo

if TYPE_CHECKING:
    from .....animations_model.model.animations.animation_frame_model import AnimationFrameModel
    from .....animations_model.model.armature.unified_armature_model import UnifiedArmatureModel
    from .....animations_model.model.blender_poses.blender_consolidated_pose_mode_animation_frame_model import \
        BlenderConsolidatedPoseModeAnimationFrameModel


class AnimationFrameModelToBlenderPoseModeAnimationFrameModelConverter:
    def derive_using_consolidation_of_armature_models_with_home_positioning(
            self,
            unified_armature_model: 'UnifiedArmatureModel',
            animation_frame_model: 'AnimationFrameModel',
            armature_offsets_from_center: Tuple[float, float, float]) ->\
            'BlenderConsolidatedPoseModeAnimationFrameModel':
        unified_armature_model = unified_armature_model.translate_to_space_model(
            base_space_model=ModelSpacesInfo.MODEL_AXIS_INFO,
            target_space_model=ModelSpacesInfo.BLENDER_AXIS_INFO
        )
        unified_armature_model = unified_armature_model.set_local_offsets_to_home_values()

        animation_frame_model_nodes_hierarchy = \
            animation_frame_model.get_nodes_hierarchy()\
            .\
            translate_absolute_offsets_by(
                    offset_x=-armature_offsets_from_center[0],
                    offset_y=-armature_offsets_from_center[1],
                    offset_z=-armature_offsets_from_center[2]
            ).\
            translate_to_space_model(
                    base_space_model=ModelSpacesInfo.MODEL_AXIS_INFO,
                    target_space_model=ModelSpacesInfo.BLENDER_AXIS_INFO
            ).\
            set_local_offsets_to_home_values()

        blender_consolidated_pose_mode_animation_frame_model = FrameModelConsolidator() \
            .consolidate(
                unified_armature_model_nodes_hierarchy=unified_armature_model.nodes_hierarchy,
                animation_frame_model_nodes_hierarchy=animation_frame_model_nodes_hierarchy
            )
        return blender_consolidated_pose_mode_animation_frame_model
