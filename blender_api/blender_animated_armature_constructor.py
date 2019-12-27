from typing import TYPE_CHECKING, Tuple, Dict
from bpy.types import Object

from ..blender_api.blender_operations.general_api_operations.blender_editor_manipulation import BlenderEditorManipulation
from ..blender_api.blender_armature_constructor import BlenderArmatureConstructor
from ..blender_api.blender_operations.constructing_animations.blender_armature_animation_constructor import \
    BlenderArmatureAnimationConstructor
from ..blender_api.blender_operations.constructing_animations.deriving_pose.\
    animation_frame_to_blender_pose_mode_model_converter import \
    AnimationFrameModelToBlenderPoseModeAnimationFrameModelConverter
from ..utils.model_spaces_integration.model_spaces_info import ModelSpacesInfo

if TYPE_CHECKING:
    from ..animations_model.model.animations.animation_frame_model import AnimationFrameModel
    from ..animations_model.model.armature.unified_armature_model import UnifiedArmatureModel
    from ..animations_model.model.armature_with_animation_clips_model import ArmatureWithAnimationClipsModel


class BlenderAnimatedArmatureConstructor:
    ARMATURE_NAME = "OPENSPACE_MODEL_ARMATURE"

    def apply_armature_with_animation_clips_model(self,
                                                  armature_animation_clips_model: 'ArmatureWithAnimationClipsModel'):
        unified_armature_model = armature_animation_clips_model.get_unified_armature_model()
        armature_offsets_from_center = unified_armature_model.get_offsets_from_center_of_coordinates_system()
        unified_armature_model = unified_armature_model.bring_to_center_of_coordinates_system()
        blender_edit_mode_armature_model = unified_armature_model.get_blender_edit_mode_armature_model(
            base_space_model=ModelSpacesInfo.MODEL_AXIS_INFO)
        blender_armature_constructor = BlenderArmatureConstructor()
        armature, armature_obj = blender_armature_constructor.build_armature(
            blender_edit_mode_armature_model=blender_edit_mode_armature_model,
            name=self.ARMATURE_NAME)
        animation_clips = armature_animation_clips_model.get_animation_clips()

        blender_editor_manipulation = BlenderEditorManipulation()
        blender_editor_manipulation.enter_pose_mode()

        blender_editor_manipulation.set_context_area_ui_type_to_dopesheet()
        blender_editor_manipulation.set_context_space_data_ui_mode_to_action()

        for animation_clip_name in animation_clips:
            action = blender_editor_manipulation.enter_animation_clip(name=animation_clip_name)
            blender_editor_manipulation.set_armature_active_action(armature_obj, action)
            animation_frames = animation_clips[animation_clip_name].get_animation_frames()

            animation_frame_index_counter = 1
            keyframe_period = 3

            print("Animation clip: {}".format(animation_clip_name))

            for animation_frame_number in animation_frames:
                if (animation_frame_index_counter - 1) % keyframe_period == 0 or\
                        animation_frame_index_counter == self._get_last_frame_number(animation_frames):
                    print("Frame: {}".format(animation_frame_index_counter))
                    animation_frame = animation_frames[animation_frame_number]
                    blender_editor_manipulation.enter_frame_number(frame_number=animation_frame_number)
                    self.add_animation_frame_to_animation_clip_of_armature(
                        unified_armature_model,
                        animation_frame,
                        armature_obj,
                        armature_offsets_from_center)
                animation_frame_index_counter += 1

    def add_animation_frame_to_animation_clip_of_armature(
            self,
            unified_armature_model: 'UnifiedArmatureModel',
            animation_frame_model: 'AnimationFrameModel',
            armature_obj: Object,
            armature_offsets_from_center: Tuple[float, float, float]):
        blender_pose_mode_animation_frame_model = \
            AnimationFrameModelToBlenderPoseModeAnimationFrameModelConverter().\
            derive_using_consolidation_of_armature_models_with_home_positioning(
                unified_armature_model=unified_armature_model,
                animation_frame_model=animation_frame_model,
                armature_offsets_from_center=armature_offsets_from_center
            )

        blender_armature_animation_constructor = BlenderArmatureAnimationConstructor()
        blender_armature_animation_constructor.setup_keyframe_in_animation_clip(
            blender_pose_mode_animation_frame_model,
            armature_obj
        )

    def _get_last_frame_number(self, animation_frames: Dict[int, 'AnimationFrameModel']) -> int:
        return max(list(animation_frames.keys()))
