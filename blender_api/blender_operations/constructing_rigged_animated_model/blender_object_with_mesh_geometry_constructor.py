import array
from typing import List

import bpy
from bpy.types import Object, MeshUVLoopLayer, Image, Node

from ....utils.model_spaces_integration.vector3d import Vector3d
from ....model.objects.model.animated_export_object_model_description.materials_description.texture import Color
from ....utils.model_spaces_integration.vector2d import Vector2d
from ....model.objects.model.animated_export_object_model_description.materials_description.material import Material
from ....blender_api.blender_operations.general_api_operations.blender_objects_manipulation import \
    BlenderObjectsManipulation
from ....model.objects.model.animated_export_object_model_description.mesh_geometry import MeshGeometry
from ....model.objects.model.animated_export_object_model import AnimatedExportObjectModel


class BlenderImageHelper:
    def get_blender_image(self, width: int, height: int,
                          image_name: str,
                          texture_image_definition: List[Color]) -> Image:
        blender_image = bpy.data.images.new(name=image_name, width=width, height=height, alpha=True)  # type: Image
        pixel_index = 0
        pixels_array = array.array('f',(0,)*len(texture_image_definition) * 4)
        for pixel_color in texture_image_definition:
            pixels_array[pixel_index] = pixel_color.red
            pixels_array[pixel_index + 1] = pixel_color.green
            pixels_array[pixel_index + 2] = pixel_color.blue
            pixels_array[pixel_index + 3] = pixel_color.alpha
            pixel_index += 4

        blender_image.pixels = pixels_array.tolist()
        blender_image.pack()
        return blender_image


class BlenderMeshMaterialApplier:
    def _apply_uv_map(self, uv_map: List[Vector2d], mesh_obj: Object,
                      animated_export_object: AnimatedExportObjectModel) -> MeshUVLoopLayer:
        uv_loops_layer = mesh_obj.data.uv_layers.new(name=animated_export_object.name + "_UV")  # type: MeshUVLoopLayer

        uv_loop_index = 0
        while uv_loop_index < len(uv_map):
            first_vertex_uv = uv_map[uv_loop_index]
            second_vertex_uv = uv_map[uv_loop_index + 2]
            third_vertex_uv = uv_map[uv_loop_index + 1]

            uv_loops_layer.data[uv_loop_index].uv[0] = first_vertex_uv.x
            uv_loops_layer.data[uv_loop_index].uv[1] = first_vertex_uv.y

            uv_loops_layer.data[uv_loop_index + 1].uv[0] = second_vertex_uv.x
            uv_loops_layer.data[uv_loop_index + 1].uv[1] = second_vertex_uv.y

            uv_loops_layer.data[uv_loop_index + 2].uv[0] = third_vertex_uv.x
            uv_loops_layer.data[uv_loop_index + 2].uv[1] = third_vertex_uv.y

            uv_loop_index += 3

        return uv_loops_layer

    def apply(self, material: Material, uv_map: List[Vector2d], mesh_obj: Object,
              animated_export_object: AnimatedExportObjectModel):
        blender_material_data_block = bpy.data.materials.new(
            name=animated_export_object.name + "_MAT_" + material.name)  # type: bpy.types.Material
        blender_material_data_block.use_nodes = True

        blender_material_data_block.node_tree.nodes.clear()

        material_output_node = blender_material_data_block.\
            node_tree.nodes.new(type="ShaderNodeOutputMaterial")  # type: Node
        material_diffuse_node = blender_material_data_block.\
            node_tree.nodes.new(type="ShaderNodeBsdfDiffuse")  # type: Node
        texture_image_node = blender_material_data_block.\
            node_tree.nodes.new(type='ShaderNodeTexImage')  # type: Node
        texture_image_node.image = BlenderImageHelper().get_blender_image(
            width=material.main_texture.width,
            height=material.main_texture.height,
            texture_image_definition=material.main_texture.pixels,
            image_name=animated_export_object.name + "_" + material.name + "_" + material.main_texture.name + "_IMAGE"
        )

        uv_loops_layer = \
            self._apply_uv_map(
                uv_map=uv_map, mesh_obj=mesh_obj,
                animated_export_object=animated_export_object)  # type: MeshUVLoopLayer

        uv_map_node = blender_material_data_block.node_tree.nodes.new(type="ShaderNodeUVMap")
        uv_map_node.uv_map = uv_loops_layer.name

        blender_material_data_block.node_tree.links.new(material_output_node.inputs['Surface'],
                                                        material_diffuse_node.outputs['BSDF'])
        blender_material_data_block.node_tree.links.new(material_diffuse_node.inputs['Color'],
                                                        texture_image_node.outputs['Color'])
        blender_material_data_block.node_tree.links.new(texture_image_node.inputs['Vector'],
                                                        uv_map_node.outputs['UV'])

        mesh_obj.data.materials.append(blender_material_data_block)


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
                len([x for x in animated_export_object.mesh_geometry.uv_maps if len(x) > 0]) == 1:
            blender_mesh_material_applier = BlenderMeshMaterialApplier()
            blender_mesh_material_applier.apply(
                material=animated_export_object.materials[0],
                uv_map=animated_export_object.get_valid_uv_map(),
                mesh_obj=mesh_obj,
                animated_export_object=animated_export_object)

    def _apply_normals(self, animated_export_object: AnimatedExportObjectModel, mesh_obj: Object):
        normals_definitions = animated_export_object.mesh_geometry.normals  # type: List[Vector3d]
        for mesh_vertex_index, mesh_vertex in enumerate(mesh_obj.data.vertices):
            mesh_vertex.normal[0] = normals_definitions[mesh_vertex_index].x
            mesh_vertex.normal[1] = normals_definitions[mesh_vertex_index].y
            mesh_vertex.normal[2] = normals_definitions[mesh_vertex_index].z
