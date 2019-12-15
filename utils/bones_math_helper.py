from enum import Enum
from typing import Tuple


class AxisDirection(Enum):
    INCREASING_VALUES = 1
    DECREASING_VALUES = 2


class Axis(Enum):
    X = 1
    Y = 2
    Z = 3


class AxisInfo:
    def __init__(self,
                 forward_axis: int,
                 up_axis: int,
                 side_axis: int,
                 right_direction_values: int,
                 forward_direction_values: int,
                 up_direction_values: int):
        self.forward_axis = forward_axis  # type: int
        self.up_axis = up_axis  # type: int
        self.side_axis = side_axis  # type: int
        self.right_direction_values = right_direction_values  # type: int
        self.forward_direction_values = forward_direction_values  # type: int
        self.up_direction_values = up_direction_values  # type: int


class BonesMathHelper:
    @classmethod
    def calculate_head_and_tail_position(
            cls,
            position: Tuple[float, float, float],
            rotation: Tuple[float, float, float],
            scale: Tuple[float, float, float],
            model_axis_info: AxisInfo,
            blender_axis_info: AxisInfo) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        # Let's assume first that position given is in the middle of bone's length, in the half-way from tail to bone
        # and vice versa
        head_position = (0.0, 0.0, 0.0)
        tail_position = (0.0, 0.0, 0.0)

        return head_position, tail_position

