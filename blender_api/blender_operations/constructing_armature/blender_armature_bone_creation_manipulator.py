from typing import Tuple

import bpy
from bpy.types import Armature, EditBone


class BlenderArmatureBoneCreationManipulator:
    def enter_edit_mode(self):
        bpy.ops.object.mode_set(mode='EDIT')

    def add_bone(self,
                 head_position: Tuple[float, float, float],
                 tail_position: Tuple[float, float, float],
                 armature: Armature,
                 name: str):
        edit_bone = armature.edit_bones.new(name=name)  # type: EditBone
        edit_bone.head[0] = head_position[0]
        edit_bone.head[1] = head_position[1]
        edit_bone.head[2] = head_position[2]

        edit_bone.tail[0] = tail_position[0]
        edit_bone.tail[1] = tail_position[1]
        edit_bone.tail[2] = tail_position[2]

    def _find_bone_with_name(self, armature: Armature, name: str) -> EditBone:
        for edit_bone in armature.edit_bones:
            if edit_bone.name == name:
                return edit_bone
        raise Exception("Did not find bone with that name!")

    def parent_bone_to(self, armature: Armature, child_bone_name: str, parent_bone_name: str):
        child_edit_bone = self._find_bone_with_name(armature, child_bone_name)  # type: EditBone
        parent_edit_bone = self._find_bone_with_name(armature, parent_bone_name)  # type: EditBone
        child_edit_bone.parent = parent_edit_bone
