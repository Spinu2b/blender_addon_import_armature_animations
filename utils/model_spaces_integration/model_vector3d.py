import copy
from typing import TYPE_CHECKING

from ...utils.model_spaces_integration.axis import Axis
from ...utils.model_spaces_integration.euler_rotation_model_vector3d import EulerRotationModelVector3d
from ...utils.model_spaces_integration.vector3d import Vector3d

if TYPE_CHECKING:
    from ...utils.model_spaces_integration.axis_direction import AxisDirection
    from ...utils.model_spaces_integration.axis_info import AxisInfo


class ModelVector3d:
    def __init__(self, axis_info: 'AxisInfo', x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x  # type: float
        self.y = y  # type: float
        self.z = z  # type: float
        self.axis_info = copy.deepcopy(axis_info)  # type: AxisInfo

    def get_forward_axis_value(self) -> float:
        if self.get_forward_axis() == Axis.X:
            return self.x
        elif self.get_forward_axis() == Axis.Y:
            return self.y
        elif self.get_forward_axis() == Axis.Z:
            return self.z

    def get_forward_axis(self) -> Axis:
        return self.axis_info.forward_axis

    def get_forward_axis_direction(self) -> 'AxisDirection':
        return self.axis_info.forward_direction_values

    def get_up_axis_value(self) -> float:
        if self.get_up_axis() == Axis.X:
            return self.x
        elif self.get_up_axis() == Axis.Y:
            return self.y
        elif self.get_up_axis() == Axis.Z:
            return self.z

    def get_up_axis(self) -> Axis:
        return self.axis_info.up_axis

    def get_up_axis_direction(self) -> 'AxisDirection':
        return self.axis_info.up_direction_values

    def get_side_axis_value(self) -> float:
        if self.get_side_axis() == Axis.X:
            return self.x
        elif self.get_side_axis() == Axis.Y:
            return self.y
        elif self.get_side_axis() == Axis.Z:
            return self.z

    def get_side_axis(self) -> Axis:
        return self.axis_info.side_axis

    def get_side_axis_right_direction(self) -> 'AxisDirection':
        return self.axis_info.right_direction_values

    def set_forward_axis_value(self, value: float, flip_value: bool):
        value = value if not flip_value else -value
        if self.get_forward_axis() == Axis.X:
            self.x = value
        elif self.get_forward_axis() == Axis.Y:
            self.y = value
        elif self.get_forward_axis() == Axis.Z:
            self.z = value

    def set_side_axis_value(self, value: float, flip_value: bool):
        value = value if not flip_value else -value
        if self.get_side_axis() == Axis.X:
            self.x = value
        elif self.get_side_axis() == Axis.Y:
            self.y = value
        elif self.get_side_axis() == Axis.Z:
            self.z = value

    def set_up_axis_value(self, value: float, flip_value: bool):
        value = value if not flip_value else -value
        if self.get_up_axis() == Axis.X:
            self.x = value
        elif self.get_up_axis() == Axis.Y:
            self.y = value
        elif self.get_up_axis() == Axis.Z:
            self.z = value

    def translate_to_model_axis(self, target_axis_info: 'AxisInfo'):
        forward_axis_value, forward_axis_direction = self.get_forward_axis_value(), self.get_forward_axis_direction()
        side_axis_value, side_axis_direction = self.get_side_axis_value(), self.get_side_axis_right_direction()
        up_axis_value, up_axis_direction = self.get_up_axis_value(), self.get_up_axis_direction()
        result = ModelVector3d(axis_info=target_axis_info)
        result.set_forward_axis_value(value=forward_axis_value,
                                      flip_value=forward_axis_direction != target_axis_info.forward_direction_values)
        result.set_side_axis_value(value=side_axis_value,
                                   flip_value=side_axis_direction != target_axis_info.right_direction_values)
        result.set_up_axis_value(value=up_axis_value,
                                 flip_value=up_axis_direction != target_axis_info.up_direction_values)
        return result

    def to_vector3d(self) -> Vector3d:
        return Vector3d(x=self.x, y=self.y, z=self.z)

    def to_euler_rotation_model_vector3d(self) -> EulerRotationModelVector3d:
        return EulerRotationModelVector3d(self)
