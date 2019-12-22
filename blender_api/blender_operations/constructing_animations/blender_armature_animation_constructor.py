from ....blender_api.blender_operations.constructing_animations.blender_animation_clips_editor_manipulator import \
    BlenderAnimationClipsEditorManipulator
from ....blender_api.blender_operations.constructing_animations.blender_armature_bone_pose_phase_manipulator import \
    BlenderArmatureBonePosePhaseManipulator
from ....blender_api.blender_operations.constructing_animations.blender_armature_bone_pose_setter_facade import \
    BlenderArmatureBonePoseSetterFacade


class BlenderArmatureAnimationConstructor:
    def setup_keyframe_in_animation_clip(self, animation_clip_name, animation_frame_number,
                                         animation_frame_model):
        blender_armature_bone_pose_phase_manipulator = BlenderArmatureBonePosePhaseManipulator()
        blender_armature_bone_pose_facade = BlenderArmatureBonePoseSetterFacade()
        blender_animation_clips_editor_manipulator = BlenderAnimationClipsEditorManipulator()
        blender_animation_clips_editor_manipulator.set_editor_context_to(
            animation_clip_name, animation_frame_number
        )
        for animation_frame_armature_bone_model in animation_frame_model.iterate_from_parent_bones_to_children():
            blender_armature_bone_pose_facade.position_bone_in_animation_frame(
                animation_frame_armature_bone_model
            )
