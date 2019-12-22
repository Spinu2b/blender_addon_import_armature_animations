import bpy
from bpy.types import Armature


class BlenderArmatureManipulator:
    def create_armature(self, name: str) -> Armature:
        return bpy.data.armatures.new(name=name)
