def register_properties():
    import bpy
    bpy.types.Scene.animations_json_path = bpy.props.StringProperty(
        description="Chemin vers le fichier JSON des animations",
        subtype='FILE_PATH'
    )
    bpy.types.Scene.objects_library_json_path = bpy.props.StringProperty(
        description="Chemin vers le fichier JSON des objets",
        subtype='FILE_PATH'
    )
    bpy.types.Scene.import_hierarchical_armature = bpy.props.BoolProperty(
        name="Exact hierarchical armature",
        description="Hierarchical armature keyed with local transforms: reproduces Raymap exactly, including the "
                    "shear of squash & stretch animations. Off: the old flat armature posed in world space",
        default=True
    )

def unregister_properties():
    import bpy
    del bpy.types.Scene.animations_json_path
    del bpy.types.Scene.objects_library_json_path
    del bpy.types.Scene.import_hierarchical_armature
import bpy


class AddonPanel(bpy.types.Panel):
    bl_idname = "spinu2b_addon_panel"
    bl_label = "spinu2b_addon_panel_label"
    bl_category = "Import armature addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Animations JSON Path:")
        layout.prop(context.scene, "animations_json_path", text="")
        layout.label(text="Objects Library JSON Path:")
        layout.prop(context.scene, "objects_library_json_path", text="")
        layout.prop(context.scene, "import_hierarchical_armature")
        row = layout.row()
        row.operator("view3d.import_animated_armature", text="Import animated armature from Raymap")
