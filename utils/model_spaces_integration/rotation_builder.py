from enum import Enum
from math import sin, cos

try:
    from .quaternion import Quaternion
    from .vector3d import Vector3d
except ValueError:
    from utils.model_spaces_integration.quaternion import Quaternion
    from utils.model_spaces_integration.vector3d import Vector3d


class AngleUnit(Enum):
    DEGREES = 1
    RADIANS = 2


class RotationBuilder:
    def __init__(self):
        self.result = Quaternion()

    def set_rotation_axis_and_angle(self, axis: Vector3d, angle: float, angle_unit: AngleUnit, counterclockwise: bool):
        axis = axis.normalized()

        if angle_unit == AngleUnit.DEGREES:
            angle = angle * 0.01745329252  # convert degrees to radians

        if not counterclockwise:
            angle = -angle

        self.result.x = axis.x * sin(angle/2)
        self.result.y = axis.y * sin(angle/2)
        self.result.z = axis.z * sin(angle/2)
        self.result.w = cos(angle/2)
        return self

    def build(self) -> Quaternion:
        return self.result
