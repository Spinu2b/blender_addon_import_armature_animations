from typing import List

import bpy
from bpy.types import Object, MeshUVLoopLayer, ImageTexture, Image

from ....model.objects.model.animated_export_object_model_description.materials_description.texture import Color
from ....utils.model_spaces_integration.vector2d import Vector2d
from ....model.objects.model.animated_export_object_model_description.materials_description.material import Material
from ....blender_api.blender_operations.general_api_operations.blender_objects_manipulation import \
    BlenderObjectsManipulation
from ....model.objects.model.animated_export_object_model_description.mesh_geometry import MeshGeometry
from ....model.objects.model.animated_export_object_model import AnimatedExportObjectModel


class BlenderImageHelper:
    def get_blender_image(self, width: int, height: int,
                          texture_image_definition: List[Color]) -> Image:
        raise NotImplementedError


class BlenderMeshMaterialApplier:
    def _apply_uv_map(self, uv_map: List[Vector2d], mesh_obj: Object,
                      animated_export_object: AnimatedExportObjectModel) -> MeshUVLoopLayer:
        uv_loops_layer = mesh_obj.data.uv_layers.new(name=animated_export_object.name + "_UV")  # type: MeshUVLoopLayer
        for uv_loop_index, uv_loop in uv_loops_layer.data.items():
            uv_loop.uv[0] = uv_map[uv_loop_index].x
            uv_loop.uv[1] = uv_map[uv_loop_index].y

        return uv_loops_layer

    def apply(self, material: Material, uv_map: List[Vector2d], mesh_obj: Object,
              animated_export_object: AnimatedExportObjectModel):
        blender_material_data_block = bpy.data.materials.new(
            name=animated_export_object.name + "_MAT_" + material.name)  # type: bpy.types.Material
        blender_material_data_block.use_nodes = True

        material_output_node = blender_material_data_block.node_tree.nodes.new(type="ShaderNodeOutputMaterial")
        material_diffuse_node = blender_material_data_block.node_tree.nodes.new(type="ShaderNodeBsdfDiffuse")
        texture_image_node = blender_material_data_block.node_tree.nodes.new(type='ShaderNodeTexImage')
        texture_image_node.image = BlenderImageHelper().get_blender_image(
            width=material.main_texture.width,
            height=material.main_texture.height,
            texture_image_definition=material.main_texture.pixels
        )

        uv_loops_layer = \
            self._apply_uv_map(
                uv_map=uv_map, mesh_obj=mesh_obj,
                animated_export_object=animated_export_object)  # type: MeshUVLoopLayer

        uv_map_node = blender_material_data_block.node_tree.nodes.new(type="ShaderNodeUVMap")
        uv_map_node.uv_map = uv_loops_layer.name

        blender_material_data_block.node_tree.links.new(material_output_node.inputs['Surface'],
                                                        material_diffuse_node['BSDF'])
        blender_material_data_block.node_tree.links.new(material_diffuse_node.inputs['Color'],
                                                        texture_image_node.outputs['Color'])
        blender_material_data_block.node_tree.links.new(texture_image_node.inputs['Vector'],
                                                        uv_map_node.outputs['UV'])

        mesh_obj.data.materials.append(blender_material_data_block)
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
        self._apply_normals(animated_export_object, mesh_obj)

        self._apply_mesh_materials(animated_export_object, mesh_obj)
        return mesh_obj

    def _apply_mesh_materials(self, animated_export_object: AnimatedExportObjectModel, mesh_obj: Object):
        if len(animated_export_object.materials) > 1:
            raise ValueError("More than one material per submesh is not supported!")
        if len([x for x in animated_export_object.mesh_geometry.uv_maps if len(x) > 0]) > 1:
            raise ValueError("More than one uv map per submesh is not supported!")
        if len(animated_export_object.materials) == 1 and \
                len([x for x in animated_export_object.mesh_geometry.uv_maps if len(x) > 0]) == 0:
            BlenderMeshMaterialApplier().apply(
                material=animated_export_object.materials[0],
                uv_map=animated_export_object.get_valid_uv_map(),
                mesh_obj=mesh_obj)

    def _apply_normals(self, animated_export_object: AnimatedExportObjectModel, mesh_obj: Object):
        raise NotImplementedError
