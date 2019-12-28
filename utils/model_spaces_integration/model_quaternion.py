import copy

from ...utils.model_spaces_integration.axis_info import AxisInfo
from ...utils.model_spaces_integration.model_vector3d import ModelVector3d
from ...utils.model_spaces_integration.quaternion import Quaternion


class ModelQuaternion:
    def __init__(self, w: float, x: float, y: float, z: float, axis_info: AxisInfo):
        self.w = w  # type: float
        self.model_vector = ModelVector3d(x=x, y=y, z=z, axis_info=axis_info)

    def translate_to_model_axis(self, target_axis_info: 'AxisInfo'):
        result = copy.deepcopy(self)
        result.model_vector = result.model_vector.translate_to_model_axis(target_axis_info=target_axis_info)
        return result

    def to_quaternion(self):
        vector3d = self.model_vector.to_vector3d()
        return Quaternion(w=self.w, x=vector3d.x, y=vector3d.y, z=vector3d.z)
