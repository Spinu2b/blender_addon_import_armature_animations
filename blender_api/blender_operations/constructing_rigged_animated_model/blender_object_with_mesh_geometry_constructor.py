import bpy
from bpy.types import Object

from ....model.objects.model.animated_export_object_model_description.materials_description.material import Material
from ....blender_api.blender_operations.general_api_operations.blender_objects_manipulation import \
    BlenderObjectsManipulation
from ....model.objects.model.animated_export_object_model_description.mesh_geometry import MeshGeometry
from ....model.objects.model.animated_export_object_model import AnimatedExportObjectModel


class BlenderMeshMaterialApplier:
    def apply(self, material: Material):
        raise NotImplementedError


class BlenderObjectWithMeshGeometryConstructor:
    def construct(self, animated_export_object: AnimatedExportObjectModel) -> Object:
        blender_objects_manipulation = BlenderObjectsManipulation()
        mesh_data_block = bpy.data.meshes.new(name=animated_export_object.name)
        mesh_obj = blender_objects_manipulation.create_new_object_with_linked_datablock(
            object_name=animated_export_object.name + "_OBJECT", data_block=mesh_data_block)
        blender_objects_manipulation.link_object_to_the_scene(mesh_obj)

        blender_objects_manipulation.deselect_all_objects()
        blender_objects_manipulation.set_active_object_to(mesh_obj)
        blender_objects_manipulation.select_active_object()

        mesh_geometry = animated_export_object.mesh_geometry  # type: MeshGeometry

        vertices, edges, faces = mesh_geometry.get_blender_pydata_form()

        mesh_obj.data.from_pydata(vertices, edges, faces)

        self._apply_mesh_materials(animated_export_object)
        return mesh_obj

    def _apply_mesh_materials(self, animated_export_object: AnimatedExportObjectModel):
        if len(animated_export_object.materials) > 1:
            raise ValueError("More than one material per submesh is not supported!")
        if len(animated_export_object.materials) == 1:
            BlenderMeshMaterialApplier().apply(animated_export_object.materials[0])
