from typing import TYPE_CHECKING

import bpy
from bpy.types import Armature, Action

if TYPE_CHECKING:
    from ....animations_model.model.armature.nodes_hierarchy.node import Node


class BlenderArmatureBonePoseSetterFacade:
    def position_bone_in_animation_frame(
            self,
            armature: Armature,
            animation_frame_armature_bone_model: 'Node'):
        raise NotImplementedError

    def lock_rotation_scale_position(self):
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')

    def select_all_pose_bones(self):
        bpy.ops.pose.select_all(action='SELECT')
