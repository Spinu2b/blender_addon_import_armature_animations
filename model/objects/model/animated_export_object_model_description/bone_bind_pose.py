import copy

from .....utils.model_spaces_integration.model_quaternion import ModelQuaternion
from .....utils.model_spaces_integration.model_vector3d import ModelVector3d
from .....utils.model_spaces_integration.quaternion import Quaternion
from .....utils.model_spaces_integration.vector3d import Vector3d
from .....utils.model_spaces_integration.axis_info import AxisInfo


class BoneBindPose:
    def __init__(
            self,
            position: Vector3d = Vector3d(0.0, 0.0, 0.0),
            rotation: Quaternion = Quaternion(1.0, 0.0, 0.0, 0.0),
            scale: Vector3d = Vector3d(1.0, 1.0, 1.0)):
        self.position = copy.deepcopy(position)  # type: Vector3d
        self.rotation = copy.deepcopy(rotation)  # type: Quaternion
        self.scale = copy.deepcopy(scale)  # type: Vector3d

    def translate_to_space_model(self, base_space_model: AxisInfo, target_space_model: AxisInfo):
        self.position = ModelVector3d(x=self.position.x, y=self.position.y, z=self.position.z,
                                      axis_info=base_space_model).\
            translate_to_model_axis(target_axis_info=target_space_model).to_vector3d()
        self.rotation = ModelQuaternion(w=self.rotation.w, x=self.rotation.x, y=self.rotation.y, z=self.rotation.z,
                                        axis_info=base_space_model).\
            translate_to_model_axis(target_axis_info=target_space_model).to_quaternion()
        self.scale = ModelVector3d(
            x=self.scale.x, y=self.scale.y, z=self.scale.z, axis_info=base_space_model).\
            translate_to_model_axis(target_axis_info=target_space_model).to_vector3d()
