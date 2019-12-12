from blender_api.blender_armature_constructor import BlenderArmatureConstructor
from blender_api.blender_operations.constructing_animations.blender_armature_animation_constructor import \
    BlenderArmatureAnimationConstructor
from blender_api.blender_operations.constructing_animations.deriving_pose.\
    animation_frame_model_to_blender_pose_mode_animation_frame_model_converter import \
    AnimationFrameModelToBlenderPoseModeAnimationFrameModelConverter


class BlenderAnimatedArmatureConstructor:
    def apply_armature_with_animation_clips_model(self, armature_animation_clips_model):
        unified_armature_model = armature_animation_clips_model.get_unified_armature_model()
        blender_edit_mode_armature_model = unified_armature_model.get_blender_edit_mode_armature_model()
        blender_armature_constructor = BlenderArmatureConstructor()
        blender_armature_constructor.build_armature(blender_edit_mode_armature_model)
        for animation_clip in armature_animation_clips_model.get_animation_clips():
            for animation_frame in animation_clip.get_animation_frames():
                self.add_animation_frame_to_animation_clip_of_armature(
                    blender_edit_mode_armature_model,
                    unified_armature_model,
                    animation_clip.name,
                    animation_frame.index,
                    animation_frame)

    def add_animation_frame_to_animation_clip_of_armature(
            self,
            blender_edit_mode_armature_model,
            unified_armature_model,
            animation_clip_name,
            animation_frame_number,
            animation_frame_model):
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
