from typing import TYPE_CHECKING, Tuple
from bpy.types import Armature, Object

from ....model.animations.model.blender_edit_mode_armature_model import BlenderEditModeArmatureNodeModel
from ....blender_api.blender_operations.general_api_operations.blender_editor_manipulation import BlenderEditorManipulation
from ....blender_api.blender_operations.constructing_armature.blender_armature_bone_creation_manipulator import \
    BlenderArmatureBoneCreationManipulator
from ....blender_api.blender_operations.constructing_armature.blender_armature_manipulator import\
    BlenderArmatureManipulator


class BlenderArmatureGenerator:
    def create_armature(self, name: str) -> Tuple[Armature, Object]:
        blender_armature_manipulator = BlenderArmatureManipulator()
        return blender_armature_manipulator.create_armature(name=name)

    def place_bone(self,
                   armature_obj: Object,
                   armature: 'Armature',
                   armature_bone_model: 'BlenderEditModeArmatureNodeModel'):
        blender_armature_bone_creation_manipulator = BlenderArmatureBoneCreationManipulator()
        blender_editor_manipulation = BlenderEditorManipulation()
        blender_editor_manipulation.enter_edit_mode()
        blender_armature_bone_creation_manipulator.add_bone(
            head_position=(armature_bone_model.head_position_x,
                           armature_bone_model.head_position_y,
                           armature_bone_model.head_position_z),
            tail_position=(armature_bone_model.tail_position_x,
                           armature_bone_model.tail_position_y,
                           armature_bone_model.tail_position_z),
            position=armature_bone_model.position,
            rotation=armature_bone_model.rotation,
            scale=armature_bone_model.scale,
            name=armature_bone_model.name,
            armature=armature,
            armature_obj=armature_obj
        )

    def parent_bone_to(self,
                       child: 'BlenderEditModeArmatureNodeModel',
                       parent: 'BlenderEditModeArmatureNodeModel',
                       armature: 'Armature'):
        blender_armature_bone_creation_manipulator = BlenderArmatureBoneCreationManipulator()
        if parent is not None:
            blender_armature_bone_creation_manipulator.parent_bone_to(
                child_bone_name=child.name,
                parent_bone_name=parent.name,
                armature=armature)
