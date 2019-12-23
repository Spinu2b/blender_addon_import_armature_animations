import copy
from typing import TYPE_CHECKING

from ...utils.model_spaces_integration.vector3d import Vector3d

if TYPE_CHECKING:
    from ...utils.model_spaces_integration.axis_info import AxisInfo


class Vector3dBasingModelVector3dBuilder:
    def __init__(self, axis_info: 'AxisInfo'):
        self.axis_info = copy.deepcopy(axis_info)
        self.result = Vector3d()

    def forward_axis_value(self, value: float, forward_increasing: bool):
        return self

    def up_axis_value(self, value: float, up_increasing: bool):
        return self

    def side_right_value(self, value: float, side_right_increasing: bool):
        return self

    def build(self) -> Vector3d:
        return self.result
