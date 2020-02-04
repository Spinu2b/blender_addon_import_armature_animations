import copy
from typing import List, Tuple, Dict

from .....utils.model_spaces_integration.vector2d import Vector2d
from .....utils.model_spaces_integration.axis_info import AxisInfo
from .....utils.model_spaces_integration.model_vector3d import ModelVector3d
from .....utils.model_spaces_integration.vector3d import Vector3d


class MeshGeometry:
    def __init__(self):
        self.vertices = []  # type: List[Vector3d]
        self.triangles = []  # type: List[Tuple[int, int, int]]
        self.normals = []  # type: List[Vector3d]
        self.bones_weights = dict()  # type: Dict[str, Dict[int, float]]

        self.uv_maps = [[]]  # type: List[List[Vector2d]]

    def translate_to_space_model(self, base_space_model: AxisInfo, target_space_model: AxisInfo):
        self.vertices = [ModelVector3d(x=v.x, y=v.y, z=v.z,
                                       axis_info=base_space_model).
                         translate_to_model_axis(target_axis_info=target_space_model).to_vector3d()
                         for v in self.vertices]
        self.normals = [ModelVector3d(x=v.x, y=v.y, z=v.z,
                                      axis_info=base_space_model).
                        translate_to_model_axis(target_axis_info=target_space_model).to_vector3d()
                        for v in self.normals]

    def get_blender_pydata_form(self) -> Tuple[List[Tuple[float, float, float]], List[List[int]],
                                               List[Tuple[int, int, int]]]:
        def flatten(object):
            for item in object:
                if isinstance(item, (list)):
                    yield from flatten(item)
                else:
                    yield item
        vertices_list = [(v.x, v.y, v.z) for v in self.vertices]
        edges_list = [list(x) for x in list(set(flatten([[frozenset([f[0], f[1]]), frozenset([f[1], f[2]]),
                                                          frozenset([f[2], f[0]])] for f in
                                                         self.triangles])))]
        triangles_list = [(f[0], f[1], f[2]) for f in self.triangles]
        return vertices_list, edges_list, triangles_list
