import bpy


class AddonPanel(bpy.types.Panel):
    bl_idname = "spinu2b_addon_panel"
    bl_label = "spinu2b_addon_panel_label"
    bl_category = "Import armature addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("view3d.import_animated_armature", text="Import animated armature from Raymap")
