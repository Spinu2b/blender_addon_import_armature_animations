import bpy

from ..tests.test_quaternion_rotations import TestQuaternionRotations
from ..main import MainAddonLogic


class CreateAnimatedArmatureOperator(bpy.types.Operator):
    bl_idname = "view3d.import_animated_armature"
    bl_label = "Simple operator"
    bl_description = "Import animated armature from Raymap"

    def execute(self, context):
        MainAddonLogic().run()
        return {'FINISHED'}
