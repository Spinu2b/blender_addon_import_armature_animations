from typing import Dict

from bpy.types import Object, VertexGroup, Modifier

from ....blender_api.blender_operations.general_api_operations.blender_objects_manipulation import \
    BlenderObjectsManipulation


class BlenderRiggingHelper:
    def parent_blender_object_to_armature_with_bones_vertex_groups(
            self,
            armature_obj: Object,
            bones_vertex_groups: Dict[str, Dict[int, float]],
            blender_mesh_obj: Object):
        blender_objects_manipulation = BlenderObjectsManipulation()
        blender_objects_manipulation.parent_object_to(child=blender_mesh_obj, parent=armature_obj)

        for vertex_group_name in bones_vertex_groups:
            vertex_group = bones_vertex_groups[vertex_group_name]
            blender_vertex_group = blender_mesh_obj.vertex_groups.new(name=vertex_group_name)  # type: VertexGroup
            for vertex_in_group_index in vertex_group:
                vertex_in_group_weight = vertex_group[vertex_in_group_index]
                blender_vertex_group.add(index=[vertex_in_group_index], weight=vertex_in_group_weight,
                                         type='ADD')

        self._add_armature_modifier(armature_obj, blender_mesh_obj)

    def _add_armature_modifier(self, armature_obj: Object, blender_mesh_obj: Object):
        armature_modifier = blender_mesh_obj.modifiers.new(name="ARMATURE_MODIFIER", type="ARMATURE")  # type: Modifier
        armature_modifier.object = armature_obj
