import bpy

from ..tests.test_armature_bones_orientation_edit_pose_modes import TestArmatureBonesOrientationEditPoseModes
from ..main import MainAddonLogic


class CreateAnimatedArmatureOperator(bpy.types.Operator):
    bl_idname = "view3d.import_animated_armature"
    bl_label = "Simple operator"
    bl_description = "Import animated armature from Raymap"

    def execute(self, context):
        #TestArmatureBonesOrientationEditPoseModes().run()
        MainAddonLogic().run()
        return {'FINISHED'}
