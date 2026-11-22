import bpy
from bpy.types import Action, Armature, Object


class BlenderEditorManipulation:
    def enter_edit_mode(self):
        bpy.ops.object.mode_set(mode='EDIT')

    def enter_pose_mode(self):
        bpy.ops.object.mode_set(mode="POSE")

    def enter_frame_number(self, frame_number: int):
        bpy.context.scene.frame_current = frame_number

    def enter_animation_clip(self, name: str) -> Action:
        action = bpy.data.actions.new(name=name)  # type: Action
        action.use_fake_user = True
        return action

    def set_context_space_data_ui_mode_to_action(self):
        bpy.context.space_data.ui_mode = 'ACTION'

    def set_context_area_ui_type_to_dopesheet(self):
        bpy.context.area.ui_type = 'DOPESHEET'

    def set_armature_active_action(self, armature_obj: Object, action: Action):
        # SpaceDopeSheetEditor.action no longer exists in newer Blender (layered/slotted actions);
        # assigning through animation_data works in 2.8x and 4.x/5.x alike.
        if armature_obj.animation_data is None:
            armature_obj.animation_data_create()
        armature_obj.animation_data.action = action
