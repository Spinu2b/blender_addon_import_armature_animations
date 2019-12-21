from animations_model.model.armature.blender.blender_edit_mode_armature_node_model import \
    BlenderEditModeArmatureNodeModel
from blender_api.blender_operations.constructing_armature.blender_armature_bone_creation_manipulator import \
    BlenderArmatureBoneCreationManipulator
from blender_api.blender_operations.constructing_armature.blender_armature_manipulator import BlenderArmatureManipulator


class BlenderArmatureGenerator:
    def create_armature(self):
        blender_armature_manipulator = BlenderArmatureManipulator()
        blender_armature_manipulator.create_armature()

    def place_bone(self, armature_bone_model: BlenderEditModeArmatureNodeModel):
        blender_armature_bone_creation_manipulator = BlenderArmatureBoneCreationManipulator()
        blender_armature_bone_creation_manipulator.enter_edit_mode()
        blender_armature_bone_creation_manipulator.set_3d_cursor_location(
            armature_bone_model.position_x,
            armature_bone_model.position_y,
            armature_bone_model.position_z
        )
        blender_armature_bone_creation_manipulator.add_bone_primitive(armature_bone_model.bone_name)
        blender_armature_bone_creation_manipulator.set_bone_scale(
            armature_bone_model.scale_x,
            armature_bone_model.scale_y,
            armature_bone_model.scale_z
        )
        blender_armature_bone_creation_manipulator.set_bone_rotation(
            armature_bone_model.rotation_x,
            armature_bone_model.rotation_y,
            armature_bone_model.rotation_z
        )