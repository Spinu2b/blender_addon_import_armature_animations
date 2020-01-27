import copy

from .....utils.model_spaces_integration.axis_info import AxisInfo
from .....utils.model_spaces_integration.model_quaternion import ModelQuaternion
from .....utils.model_spaces_integration.model_vector3d import ModelVector3d
from .....utils.model_spaces_integration.quaternion import Quaternion
from .....utils.model_spaces_integration.vector3d import Vector3d


class TransformModel:
    def __init__(
            self,
            position: Vector3d = Vector3d(0.0, 0.0, 0.0),
            rotation: Quaternion = Quaternion(1.0, 0.0, 0.0, 0.0),
            scale: Vector3d = Vector3d(1.0, 1.0, 1.0),
            local_position: Vector3d = Vector3d(0.0, 0.0, 0.0),
            local_rotation: Quaternion = Quaternion(1.0, 0.0, 0.0, 0.0),
            local_scale: Vector3d = Vector3d(1.0, 1.0, 1.0)
            ):
        self.position = copy.deepcopy(position)  # type: Vector3d
        self.rotation = copy.deepcopy(rotation)  # type: Quaternion
        self.scale = copy.deepcopy(scale)  # type: Vector3d
        self.local_position = copy.deepcopy(local_position)  # type: Vector3d
        self.local_rotation = copy.deepcopy(local_rotation)  # type: Quaternion
        self.local_scale = copy.deepcopy(local_scale)  # type: Vector3d

    def translate_to_space_model(self, base_space_model: AxisInfo, target_space_model: AxisInfo):
        result = copy.deepcopy(self)
        result.position = ModelVector3d(
            x=result.position.x, y=result.position.y, z=result.position.z,
            axis_info=base_space_model
        ).translate_to_model_axis(target_axis_info=target_space_model).to_vector3d()
        result.rotation = ModelQuaternion(
            w=result.rotation.w, x=result.rotation.x, y=result.rotation.y, z=result.rotation.z,
            axis_info=base_space_model
        ).translate_to_model_axis(target_axis_info=target_space_model).to_quaternion()
        result.scale = ModelVector3d(
            x=result.scale.x, y=result.scale.y, z=result.scale.z,
            axis_info=base_space_model
        ).translate_to_model_axis(target_axis_info=target_space_model).to_vector3d()

        result.local_position = ModelVector3d(
            x=result.local_position.x, y=result.local_position.y, z=result.local_position.z,
            axis_info=base_space_model
        ).translate_to_model_axis(target_axis_info=target_space_model).to_vector3d()
        result.local_rotation = ModelQuaternion(
            w=result.local_rotation.w, x=result.local_rotation.x, y=result.local_rotation.y, z=result.local_rotation.z,
            axis_info=base_space_model
        ).translate_to_model_axis(target_axis_info=target_space_model).to_quaternion()
        result.local_scale = ModelVector3d(
            x=result.local_scale.x, y=result.local_scale.y, z=result.local_scale.z,
            axis_info=base_space_model
        ).translate_to_model_axis(target_axis_info=target_space_model).to_vector3d()

        return result