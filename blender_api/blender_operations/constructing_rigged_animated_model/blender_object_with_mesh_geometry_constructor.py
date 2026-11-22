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

        # the UVs are per vertex: every loop takes its own vertex's UV. (Assuming loop i = vertex i broke meshes whose
        # triangles share vertices, e.g. R3's double-sided ones where each triangle comes twice, once per winding:
        # every face after the first got another face's UVs)
        loops = mesh_obj.data.loops
        loop_vertex_indices = [0] * len(loops)
        loops.foreach_get("vertex_index", loop_vertex_indices)
        loop_uvs = []
        for vertex_index in loop_vertex_indices:
            vertex_uv = uv_map[vertex_index]
            loop_uvs.append(vertex_uv.x)
            loop_uvs.append(vertex_uv.y)
        uv_loops_layer.data.foreach_set("uv", loop_uvs)

        return uv_loops_layer

    def apply(self, material: Material, uv_map: List[Vector2d], mesh_obj: Object,
              animated_export_object: AnimatedExportObjectModel):
        blender_material_data_block = bpy.data.materials.new(
            name=animated_export_object.name + "_MAT_" + material.name)  # type: bpy.types.Material
        blender_material_data_block.use_nodes = True

        blender_material_data_block.node_tree.nodes.clear()

        material_output_node = blender_material_data_block.\
            node_tree.nodes.new(type="ShaderNodeOutputMaterial")  # type: Node
        material_principled_bsdf_node = blender_material_data_block.\
            node_tree.nodes.new(type="ShaderNodeBsdfPrincipled")  # type: Node
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
                                                        material_principled_bsdf_node.outputs['BSDF'])
        blender_material_data_block.node_tree.links.new(material_principled_bsdf_node.inputs['Base Color'],
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
        non_empty_uv_maps = [x for x in animated_export_object.mesh_geometry.uv_maps if len(x) > 0]
        if len(non_empty_uv_maps) > 1:
            # R3 materials can have several texture layers, each with its UV channel; the export carries only the
            # first layer's texture (_Tex0), whose UVs are the first map: the others are not used here
            # (get_valid_uv_map takes the first one). Seen: a second map identical to the first (swamp_82 Caggarde)
            differing = [i for i, uv_map in enumerate(non_empty_uv_maps[1:], start=1)
                         if self._uv_maps_differ(non_empty_uv_maps[0], uv_map)]
            print("{}: {} UV maps, using the first one{}".format(
                animated_export_object.name, len(non_empty_uv_maps),
                "; maps {} differ from it (their texture layers are not exported)".format(differing)
                if differing else " (the others are identical)"))
        if len(animated_export_object.materials) == 1 and len(non_empty_uv_maps) >= 1:
            blender_mesh_material_applier = BlenderMeshMaterialApplier()
            blender_mesh_material_applier.apply(
                material=animated_export_object.materials[0],
                uv_map=animated_export_object.get_valid_uv_map(),
                mesh_obj=mesh_obj,
                animated_export_object=animated_export_object)

    def _uv_maps_differ(self, first, second) -> bool:
        if len(first) != len(second):
            return True
        return any(abs(a.x - b.x) > 1e-6 or abs(a.y - b.y) > 1e-6 for a, b in zip(first, second))

    def _apply_normals(self, animated_export_object: AnimatedExportObjectModel, mesh_obj: Object):
        normals_definitions = animated_export_object.mesh_geometry.normals  # type: List[Vector3d]
        normals = [(n.x, n.y, n.z) for n in normals_definitions]
        mesh_obj.data.normals_split_custom_set_from_vertices(normals)
