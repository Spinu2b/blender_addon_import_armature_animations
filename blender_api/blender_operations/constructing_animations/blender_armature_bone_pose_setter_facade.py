from typing import TYPE_CHECKING

import bpy
from bpy.types import Object, Pose, PoseBone

if TYPE_CHECKING:
    from ....animations_model.model.armature.nodes_hierarchy.node import Node


class BlenderArmatureBonePoseSetterFacade:
    def position_bone_in_animation_frame(
            self,
            armature_obj: Object,
            animation_frame_armature_bone_model: 'Node'):
        pose = armature_obj.pose  # type: Pose

        complementary_pose_bone = pose.bones.get(animation_frame_armature_bone_model.name)  # type: PoseBone

        complementary_pose_bone.rotation_mode = 'QUATERNION'

        complementary_pose_bone.location[0] = animation_frame_armature_bone_model.local_position.x
        complementary_pose_bone.location[1] = animation_frame_armature_bone_model.local_position.y
        complementary_pose_bone.location[2] = animation_frame_armature_bone_model.local_position.z

        complementary_pose_bone.rotation_quaternion[0] = animation_frame_armature_bone_model.local_rotation.w
        complementary_pose_bone.rotation_quaternion[1] = animation_frame_armature_bone_model.local_rotation.x
        complementary_pose_bone.rotation_quaternion[2] = animation_frame_armature_bone_model.local_rotation.y
        complementary_pose_bone.rotation_quaternion[3] = animation_frame_armature_bone_model.local_rotation.z

        complementary_pose_bone.scale[0] = animation_frame_armature_bone_model.local_scale.x
        complementary_pose_bone.scale[1] = animation_frame_armature_bone_model.local_scale.y
        complementary_pose_bone.scale[2] = animation_frame_armature_bone_model.local_scale.z

    def lock_rotation_scale_position(self):
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')

    def select_all_pose_bones(self):
        bpy.ops.pose.select_all(action='SELECT')
