from typing import TYPE_CHECKING
from bpy.types import Armature

from ....blender_api.blender_operations.constructing_armature.blender_armature_bone_creation_manipulator import \
    BlenderArmatureBoneCreationManipulator
from ....blender_api.blender_operations.constructing_armature.blender_armature_manipulator import\
    BlenderArmatureManipulator

if TYPE_CHECKING:
    from ....animations_model.model.armature.blender.blender_edit_mode_armature_node_model import \
        BlenderEditModeArmatureNodeModel


class BlenderArmatureGenerator:
    def create_armature(self, name: str) -> Armature:
        blender_armature_manipulator = BlenderArmatureManipulator()
        return blender_armature_manipulator.create_armature(name=name)

    def place_bone(self, armature_bone_model: 'BlenderEditModeArmatureNodeModel'):
        blender_armature_bone_creation_manipulator = BlenderArmatureBoneCreationManipulator()
        blender_armature_bone_creation_manipulator.enter_edit_mode()
        blender_armature_bone_creation_manipulator.add_bone(
            head_position=(armature_bone_model.head_position_x,
                           armature_bone_model.head_position_y,
                           armature_bone_model.head_position_z),
            tail_position=(armature_bone_model.tail_position_x,
                           armature_bone_model.tail_position_y,
                           armature_bone_model.tail_position_z),
            name=armature_bone_model.name
        )

    def parent_bone_to(self, child: 'BlenderEditModeArmatureNodeModel', parent: 'BlenderEditModeArmatureNodeModel'):
        blender_armature_bone_creation_manipulator = BlenderArmatureBoneCreationManipulator()
        if parent is not None:
            blender_armature_bone_creation_manipulator.parent_bone_to(
                child_bone_name=child.name,
                parent_bone_name=parent.name)
