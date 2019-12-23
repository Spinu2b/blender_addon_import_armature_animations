import bpy
from bpy.types import Armature


class BlenderArmatureManipulator:
    def create_armature(self, name: str) -> Armature:
        armature = bpy.data.armatures.new(name=name)
        armature_obj = bpy.data.objects.new(name + "_OBJECT", armature)
        bpy.context.collection.objects.link(armature_obj)
        bpy.context.view_layer.objects.active = armature_obj
        bpy.context.active_object.select_set(state=True)
        return armature
