import bpy
from bpy.types import Object, BlendData


class BlenderObjectsManipulation:
    def create_new_object_with_linked_datablock(self, object_name: str, data_block: BlendData) -> Object:
        return bpy.data.objects.new(object_name + "_OBJECT", data_block)

    def link_object_to_the_scene(self, object: Object):
        bpy.context.collection.objects.link(object)

    def set_active_object_to(self, object: Object):
        bpy.context.view_layer.objects.active = object

    def select_active_object(self):
        bpy.context.active_object.select_set(state=True)

    def deselect_all_objects(self):
        bpy.ops.object.select_all(action='DESELECT')
