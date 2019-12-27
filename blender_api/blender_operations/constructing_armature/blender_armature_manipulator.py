from typing import Tuple

import bpy
from bpy.types import Armature, Object

from ....blender_api.blender_operations.general_api_operations.blender_objects_manipulation import \
    BlenderObjectsManipulation


class BlenderArmatureManipulator:
    def create_armature(self, name: str) -> Tuple[Armature, Object]:
        blender_objects_manipulation = BlenderObjectsManipulation()
        armature = bpy.data.armatures.new(name=name)
        armature_obj = blender_objects_manipulation.create_new_object_with_linked_datablock(
            object_name=name + "_OBJECT", data_block=armature)
        blender_objects_manipulation.link_object_to_the_scene(armature_obj)
        blender_objects_manipulation.deselect_all_objects()
        blender_objects_manipulation.set_active_object_to(armature_obj)
        blender_objects_manipulation.select_active_object()
        return armature, armature_obj
