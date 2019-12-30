from typing import TYPE_CHECKING

try:
    from ...utils.model_spaces_integration.axis_direction import AxisDirection
    from ...utils.model_spaces_integration.model_vector3d import ModelVector3d
    from ...utils.model_spaces_integration.vector3d import Vector3d
except ValueError:
    from utils.model_spaces_integration.axis_direction import AxisDirection
    from utils.model_spaces_integration.model_vector3d import ModelVector3d
    from utils.model_spaces_integration.vector3d import Vector3d

if TYPE_CHECKING:
    from ...utils.model_spaces_integration.axis_info import AxisInfo


class Vector3dBasingModelVector3dBuilder:
    def __init__(self, axis_info: 'AxisInfo'):
        self.result_model = ModelVector3d(axis_info=axis_info)

    def forward_axis_value(self, value: float, forward_increasing: bool):
        self.result_model.set_forward_axis_value(
            value=value,
            flip_value=forward_increasing != (
                    self.result_model.get_forward_axis_direction() == AxisDirection.INCREASING_VALUES))
        return self

    def up_axis_value(self, value: float, up_increasing: bool):
        self.result_model.set_up_axis_value(
            value=value,
            flip_value=up_increasing != (
                    self.result_model.get_up_axis_direction() == AxisDirection.INCREASING_VALUES))
        return self

    def side_right_value(self, value: float, side_right_increasing: bool):
        self.result_model.set_side_axis_value(
            value=value,
            flip_value=side_right_increasing != (
                    self.result_model.get_side_axis_right_direction() == AxisDirection.INCREASING_VALUES))
        return self

    def build(self) -> Vector3d:
        return self.result_model.to_vector3d()
