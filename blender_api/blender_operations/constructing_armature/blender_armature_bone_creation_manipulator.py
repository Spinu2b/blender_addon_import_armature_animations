from typing import Tuple

import bpy


class BlenderArmatureBoneCreationManipulator:
    def enter_edit_mode(self):
        bpy.ops.object.mode_set(mode='EDIT')

    def add_bone(self,
                 head_position: Tuple[float, float, float],
                 tail_position: Tuple[float, float, float],
                 name: str):
        pass

    def parent_bone_to(self, child_bone_name: str, parent_bone_name: str):
        pass
