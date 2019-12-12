import bpy


class BlenderArmatureManipulator:
    def create_armature(self):
        bpy.ops.object.armature_add()
