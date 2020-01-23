from model.objects.model.animated_export_object_model import AnimatedExportObjectModel


class BlenderMeshBuilder:
    def place_vertex(self, vertex_index: int, x: float, y: float, z: float):
        raise NotImplementedError

    def create_triangle_face(self, vertex_index_first: int,
                             vertex_index_second: int, vertex_index_third: int):
        raise NotImplementedError


class BlenderObjectWithMeshGeometryConstructor:
    def construct(self, animated_export_object: AnimatedExportObjectModel):
        mesh_geometry = animated_export_object.mesh_geometry  # type: MeshGeometry

        blender_mesh_builder = BlenderMeshBuilder()

        for vertex_index, vertex in enumerate(mesh_geometry.vertices):
            blender_mesh_builder.place_vertex(vertex_index, vertex.x, vertex.y, vertex.z)

        for triangle in mesh_geometry.triangles:
            blender_mesh_builder.create_triangle_face(
                triangle[0], triangle[1], triangle[2]
            )
