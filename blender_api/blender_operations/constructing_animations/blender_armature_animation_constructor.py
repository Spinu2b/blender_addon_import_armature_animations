import bpy
from bpy.types import Object

from ....model.animations.model.blender_pose_mode_animation_frame_model import BlenderPoseModeAnimationFrameModel
from ....blender_api.blender_operations.constructing_animations.blender_armature_bone_pose_setter_facade import \
    BlenderArmatureBonePoseSetterFacade


class BlenderArmatureAnimationConstructor:
    def setup_keyframe_in_animation_clip(
            self,
            animation_frame_model: 'BlenderPoseModeAnimationFrameModel',
            armature_obj: Object):
        # While an action with F-curves is assigned, Blender re-evaluates it when pose matrices are set
        # (convert_space etc.) and overwrites the pose being built with the existing keys, so every frame of a
        # clip became a copy of its first frame. Detach the action while posing, then write the keys straight
        # into its F-curves.
        animation_data = armature_obj.animation_data
        action = animation_data.action if animation_data is not None else None
        if action is not None:
            animation_data.action = None

        blender_armature_bone_pose_facade = BlenderArmatureBonePoseSetterFacade()
        for animation_frame_armature_bone_model_iter in animation_frame_model.iterate_nodes():
            blender_armature_bone_pose_facade.position_bone_in_animation_frame(
                armature_obj,
                animation_frame_armature_bone_model_iter.node
            )

        frame = bpy.context.scene.frame_current
        pose_values = [(pose_bone.name,
                        tuple(pose_bone.location),
                        tuple(pose_bone.rotation_quaternion),
                        tuple(pose_bone.scale)) for pose_bone in armature_obj.pose.bones]

        if action is not None:
            animation_data.action = action
            self._write_keys(action, armature_obj, frame, pose_values)

    def _write_keys(self, action, armature_obj: Object, frame: int, pose_values):
        for bone_name, location, rotation, scale in pose_values:
            for prop, values in (("location", location), ("rotation_quaternion", rotation), ("scale", scale)):
                data_path = 'pose.bones["{}"].{}'.format(bone_name, prop)
                for index, value in enumerate(values):
                    fcurve = self._ensure_fcurve(action, armature_obj, data_path, index, bone_name)
                    fcurve.keyframe_points.insert(frame, value)

    def _ensure_fcurve(self, action, armature_obj: Object, data_path: str, index: int, group_name: str):
        if hasattr(action, "fcurve_ensure_for_datablock"):  # Blender 4.4+ (slotted actions)
            return action.fcurve_ensure_for_datablock(armature_obj, data_path, index=index, group_name=group_name)
        fcurve = action.fcurves.find(data_path, index=index)
        if fcurve is None:
            fcurve = action.fcurves.new(data_path, index=index, action_group=group_name)
        return fcurve
