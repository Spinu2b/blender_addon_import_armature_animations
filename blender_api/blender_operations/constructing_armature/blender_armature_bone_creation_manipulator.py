import bpy


class BlenderArmatureBoneHelper:
    def calculate_bone_ends_positions_for_scale(self, scale_x, scale_y, scale_z):
        pass

    def calculate_bone_ends_positions_for_rotation(self, rotation_x, rotation_y, rotation_z):
        pass


class BlenderArmatureBoneCreationManipulator:
    def enter_edit_mode(self):
        bpy.ops.object.mode_set(mode='EDIT')

    def set_3d_cursor_location(self, position_x, position_y, position_z):
        bpy.context.scene.cursor_location = (position_x, position_y, position_z)

    def add_bone_primitive(self, bone_name):
        bpy.ops.armature.bone_primitive_add(name=bone_name)

    def set_bone_scale(self, scale_x, scale_y, scale_z):
        blender_armature_bone_helper = BlenderArmatureBoneHelper()
        bone_head_pos, bone_tail_pos = blender_armature_bone_helper.\
            calculate_bone_ends_positions_for_scale(
                scale_x, scale_y, scale_z
            )

    def set_bone_rotation(self, rotation_x, rotation_y, rotation_z):
        blender_armature_bone_helper = BlenderArmatureBoneHelper()
        bone_head_pos, bone_tail_pos = blender_armature_bone_helper.\
            calculate_bone_ends_positions_for_rotation(
                rotation_x, rotation_y, rotation_z
            )
