import bpy
from bpy.types import Object, Pose, PoseBone
from mathutils import Matrix, Vector, Quaternion

from ....model.animations.model.blender_pose_mode_animation_frame_model import BlenderPoseModeAnimationFrameModelNode


class BlenderArmatureBonePoseSetterFacade:
    def position_bone_in_animation_frame(
            self,
            armature_obj: Object,
            animation_frame_armature_bone_model: 'BlenderPoseModeAnimationFrameModelNode') -> PoseBone:
        pose = armature_obj.pose  # type: Pose
        complementary_pose_bone = pose.bones.get(animation_frame_armature_bone_model.bone_name)  # type: PoseBone
        complementary_pose_bone.rotation_mode = 'QUATERNION'

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

        return complementary_pose_bone

    def lock_rotation_scale_position(self):
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')

    def select_all_pose_bones(self):
        bpy.ops.pose.select_all(action='SELECT')
