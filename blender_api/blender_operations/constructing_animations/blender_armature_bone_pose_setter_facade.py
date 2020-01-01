from typing import TYPE_CHECKING

import bpy
from bpy.types import Object, Pose, PoseBone
from mathutils import Matrix, Vector, Quaternion

from ....utils.model_spaces_integration.vector3d import Vector3d

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

        if not self._is_minimized(animation_frame_armature_bone_model.local_scale):
            loc = Matrix.Translation(Vector((
                animation_frame_armature_bone_model.position.x,
                animation_frame_armature_bone_model.position.y,
                animation_frame_armature_bone_model.position.z)))

            rot = Quaternion(Vector((
                animation_frame_armature_bone_model.rotation.w,
                animation_frame_armature_bone_model.rotation.x,
                animation_frame_armature_bone_model.rotation.y,
                animation_frame_armature_bone_model.rotation.z)),
                ).to_matrix().to_4x4()

            scale = Matrix()
            scale[0][0] = animation_frame_armature_bone_model.scale.x
            scale[1][1] = animation_frame_armature_bone_model.scale.y
            scale[2][2] = animation_frame_armature_bone_model.scale.z

            world_mat = loc @ rot @ scale

            complementary_pose_bone.matrix = armature_obj.convert_space(
                pose_bone=complementary_pose_bone,
                matrix=world_mat,
                from_space='WORLD',
                to_space='POSE')
        else:
            local_scale_minimizing = Vector3d(0.0000001, 0.0000001, 0.0000001)
            complementary_pose_bone.location[0] = 0.0
            complementary_pose_bone.location[1] = 0.0
            complementary_pose_bone.location[2] = 0.0
            complementary_pose_bone.rotation_quaternion[0] = 1.0
            complementary_pose_bone.rotation_quaternion[1] = 0.0
            complementary_pose_bone.rotation_quaternion[2] = 0.0
            complementary_pose_bone.rotation_quaternion[3] = 0.0
            complementary_pose_bone.scale[0] = local_scale_minimizing.x
            complementary_pose_bone.scale[1] = local_scale_minimizing.y
            complementary_pose_bone.scale[2] = local_scale_minimizing.z

    def lock_rotation_scale_position(self):
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')

    def select_all_pose_bones(self):
        bpy.ops.pose.select_all(action='SELECT')

    def _is_minimized(self, scale: Vector3d) -> bool:
        local_scale_minimizing = Vector3d(0.000001, 0.000001, 0.000001)
        return abs(scale.x) <= local_scale_minimizing.x and abs(scale.y) <= local_scale_minimizing.y and \
            abs(scale.z) <= local_scale_minimizing.z
