from bpy.types import Object

from ....model.animations.model.blender_pose_mode_animation_frame_model import BlenderPoseModeAnimationFrameModel
from ....blender_api.blender_operations.general_api_operations.blender_objects_manipulation import \
    BlenderObjectsManipulation
from ....blender_api.blender_operations.constructing_animations.blender_armature_bone_pose_setter_facade import \
    BlenderArmatureBonePoseSetterFacade


class BlenderArmatureAnimationConstructor:
    def setup_keyframe_in_animation_clip(
            self,
            animation_frame_model: 'BlenderPoseModeAnimationFrameModel',
            armature_obj: Object):
        blender_armature_bone_pose_facade = BlenderArmatureBonePoseSetterFacade()
        blender_objects_manipulation = BlenderObjectsManipulation()
        for animation_frame_armature_bone_model_iter in animation_frame_model.iterate_nodes():
            if animation_frame_armature_bone_model_iter.node.bone_name != "ROOT_CHANNEL" and \
                    animation_frame_armature_bone_model_iter.node.is_keyframe:
                pose_bone = blender_armature_bone_pose_facade.position_bone_in_animation_frame(
                    armature_obj,
                    animation_frame_armature_bone_model_iter.node
                )
                blender_objects_manipulation.select_pose_bone(pose_bone)
                blender_armature_bone_pose_facade.lock_rotation_scale_position()
                blender_objects_manipulation.deselect_all_pose_objects()
