from enum import Enum

from ..utils.model_spaces_integration.quaternion import Quaternion
from ..utils.model_spaces_integration.vector3d import Vector3d


class AngleUnit(Enum):
    DEGREES = 1
    RADIANS = 2


class RotationBuilder:
    def __init__(self):
        self.result = Quaternion()

    def set_rotation_axis(self, axis: Vector3d):
        raise NotImplementedError

    def set_angle(self, angle: float, angle_unit: AngleUnit, counterclockwise: bool):
        raise NotImplementedError

    def build(self) -> Quaternion:
        return self.result
