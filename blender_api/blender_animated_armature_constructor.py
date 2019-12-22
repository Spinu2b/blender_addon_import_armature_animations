from animations_model.model.animations.animation_frame_model import AnimationFrameModel
from animations_model.model.armature.blender.blender_edit_mode_armature_model import BlenderEditModeArmatureModel
from animations_model.model.armature.unified_armature_model import UnifiedArmatureModel
from animations_model.model.armature_with_animation_clips_model import ArmatureWithAnimationClipsModel
from blender_api.blender_armature_constructor import BlenderArmatureConstructor
from blender_api.blender_operations.constructing_animations.blender_armature_animation_constructor import \
    BlenderArmatureAnimationConstructor
from blender_api.blender_operations.constructing_animations.deriving_pose.\
    animation_frame_model_to_blender_pose_mode_animation_frame_model_converter import \
    AnimationFrameModelToBlenderPoseModeAnimationFrameModelConverter
from utils.model_spaces_integration.model_spaces_info import ModelSpacesInfo


class BlenderAnimatedArmatureConstructor:
    def apply_armature_with_animation_clips_model(self, armature_animation_clips_model: ArmatureWithAnimationClipsModel):
        unified_armature_model = armature_animation_clips_model.get_unified_armature_model()
        blender_edit_mode_armature_model = unified_armature_model.get_blender_edit_mode_armature_model(
            base_space_model=ModelSpacesInfo.MODEL_AXIS_INFO)
        blender_armature_constructor = BlenderArmatureConstructor()
        blender_armature_constructor.build_armature(blender_edit_mode_armature_model)
        animation_clips = armature_animation_clips_model.get_animation_clips()
        for animation_clip_name in animation_clips:
            animation_frames = animation_clips[animation_clip_name].get_animation_frames()
            for animation_frame_number in animation_frames:
                animation_frame = animation_frames[animation_frame_number]
                self.add_animation_frame_to_animation_clip_of_armature(
                    blender_edit_mode_armature_model,
                    unified_armature_model,
                    animation_clip_name,
                    animation_frame_number,
                    animation_frame)

    def add_animation_frame_to_animation_clip_of_armature(
            self,
            blender_edit_mode_armature_model: BlenderEditModeArmatureModel,
            unified_armature_model: UnifiedArmatureModel,
            animation_clip_name: str,
            animation_frame_number: int,
            animation_frame_model: AnimationFrameModel):
        blender_pose_mode_animation_frame_model = \
            AnimationFrameModelToBlenderPoseModeAnimationFrameModelConverter().\
            derive_using_consolidation_of_armature_models_with_home_positioning(
                unified_armature_model=unified_armature_model,
                blender_edit_mode_armature_model=blender_edit_mode_armature_model,
                animation_frame_model=animation_frame_model
            )

        blender_armature_animation_constructor = BlenderArmatureAnimationConstructor()
        blender_armature_animation_constructor.setup_keyframe_in_animation_clip(
            animation_clip_name,
            animation_frame_number,
            blender_pose_mode_animation_frame_model
        )
