import bpy


class BlenderEditorManipulation:
    def enter_edit_mode(self):
        bpy.ops.object.mode_set(mode='EDIT')
