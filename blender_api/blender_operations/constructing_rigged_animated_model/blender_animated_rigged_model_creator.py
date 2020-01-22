from typing import Dict

from bpy.types import Object

from blender_api.blender_operations.constructing_animations.blender_armature_animation_constructor import \
    BlenderArmatureAnimationConstructor
from blender_api.blender_operations.general_api_operations.blender_editor_manipulation import BlenderEditorManipulation
from model.animations.model.animations.animation_frame_model import AnimationFrameModel
from model.animations.model.armature_with_animation_clips_model import ArmatureWithAnimationClipsModel
from model.objects.model.animated_export_object_model import AnimatedExportObjectModel
from utils.model_spaces_integration.model_spaces_info import ModelSpacesInfo


class BlenderAnimatedRiggedModelCreator:
    ARMATURE_NAME = "OPENSPACE_MODEL_ARMATURE"

    def construct_using(self, armature_bind_pose_model: ArmatureBindPoseModel,
                        animated_export_objects: Dict[str, AnimatedExportObjectModel],
                        armature_animation_clips_model: ArmatureWithAnimationClipsModel):
        for animated_export_object_name in animated_export_objects:
            animated_export_object = animated_export_objects[animated_export_object_name]
            BlenderObjectWithMeshGeometryConstructor().construct(animated_export_object)

        blender_edit_mode_armature_model = armature_bind_pose_model.get_blender_edit_mode_armature_model(
            base_space_model=ModelSpacesInfo.MODEL_AXIS_INFO)

        blender_armature_constructor = BlenderArmatureConstructor()
        blender_armature_data_block, blender_armature_obj = blender_armature_constructor.build_armature(
            blender_edit_mode_armature_model=blender_edit_mode_armature_model,
            name=self.ARMATURE_NAME)

        for animated_export_object_name in animated_export_objects:
            animated_export_object = animated_export_objects[animated_export_object_name]
            BlenderObjectManipulator().parent_blender_object_to_armature_with_bones_vertex_groups(

            )

        BlenderObjectManipulator().join_all_objects(animated_export_objects)

        self._animate_armature_with_animation_clips(
            armature_animation_clips_model=armature_animation_clips_model,
            blender_armature_obj=blender_armature_obj
        )

    def _animate_armature_with_animation_clips(
            self,
            armature_animation_clips_model: ArmatureWithAnimationClipsModel,
            blender_armature_obj: Object):
        animation_clips = armature_animation_clips_model.get_animation_clips()

        blender_editor_manipulation = BlenderEditorManipulation()
        blender_editor_manipulation.enter_pose_mode()

        blender_editor_manipulation.set_context_area_ui_type_to_dopesheet()
        blender_editor_manipulation.set_context_space_data_ui_mode_to_action()

        for animation_clip_name in animation_clips:
            action = blender_editor_manipulation.enter_animation_clip(name=animation_clip_name)
            blender_editor_manipulation.set_armature_active_action(blender_armature_obj, action)
            animation_frames = animation_clips[animation_clip_name].get_animation_frames()

            animation_frame_index_counter = 1
            keyframe_period = 3

            print("Animation clip: {}".format(animation_clip_name))

            for animation_frame_number in animation_frames:
                if (animation_frame_index_counter - 1) % keyframe_period == 0 or \
                        animation_frame_index_counter == self._get_last_frame_number(animation_frames):
                    print("Frame: {}".format(animation_frame_index_counter))
                    animation_frame = animation_frames[animation_frame_number]
                    blender_editor_manipulation.enter_frame_number(frame_number=animation_frame_number)
                    self._add_animation_frame_to_animation_clip_of_armature(
                        animation_frame,
                        blender_armature_obj)
                animation_frame_index_counter += 1

    def _add_animation_frame_to_animation_clip_of_armature(
            self,
            animation_frame_model: 'AnimationFrameModel',
            armature_obj: Object):
        blender_pose_mode_animation_frame_model = animation_frame_model.get_blender_pose_mode_animation_frame_model()

        blender_armature_animation_constructor = BlenderArmatureAnimationConstructor()
        blender_armature_animation_constructor.setup_keyframe_in_animation_clip(
            blender_pose_mode_animation_frame_model,
            armature_obj
        )

    def _get_last_frame_number(self, animation_frames: Dict[int, 'AnimationFrameModel']) -> int:
        return max(list(animation_frames.keys()))
