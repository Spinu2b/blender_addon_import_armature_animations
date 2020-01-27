import copy
from typing import List, Tuple, Dict

from .....utils.model_spaces_integration.axis_info import AxisInfo
from .....utils.model_spaces_integration.model_vector3d import ModelVector3d
from .....utils.model_spaces_integration.vector3d import Vector3d


class MeshGeometry:
    def __init__(self):
        self.vertices = []  # type: List[Vector3d]
        self.triangles = []  # type: List[Tuple[int, int, int]]
        self.bones_weights = dict()  # type: Dict[str, Dict[int, float]]

    def translate_to_space_model(self, base_space_model: AxisInfo, target_space_model: AxisInfo):
        result = copy.deepcopy(self)
        result.vertices = [ModelVector3d(x=v.x, y=v.y, z=v.z,
                                         axis_info=base_space_model).
                           translate_to_model_axis(target_axis_info=target_space_model).to_vector3d()
                           for v in self.vertices]
        return result
