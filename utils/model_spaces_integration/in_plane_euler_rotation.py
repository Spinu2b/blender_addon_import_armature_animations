import copy
from math import cos, sin
from typing import TYPE_CHECKING
from ...utils.model_spaces_integration.axis import Axis
from ...utils.model_spaces_integration.axis_direction import AxisDirection
from ...utils.model_spaces_integration.quaternion import Quaternion
from ...utils.model_spaces_integration.vector3d import Vector3d
from ...utils.model_spaces_integration.matrix3x3 import Matrix3x3

if TYPE_CHECKING:
    from ...utils.model_spaces_integration.axis_info import AxisInfo
    from ...utils.model_spaces_integration.euler_plane import EulerPlane


class InPlaneEulerRotation:
    def __init__(self,
                 rotation_plane: 'EulerPlane',
                 rotation_axis: Axis,
                 rotation_axis_direction: AxisDirection,
                 counterclockwise_rotation: bool,
                 angle: float,
                 axis_info: 'AxisInfo'):
        self.rotation_plane = copy.deepcopy(rotation_plane)  # type: EulerPlane
        self.angle = angle  # type: float
        self.rotation_axis = rotation_axis  # type: Axis
        self.rotation_axis_direction = rotation_axis_direction  # type: AxisDirection
        self.counterclockwise_rotation = counterclockwise_rotation  # type: bool
        self.axis_info = copy.deepcopy(axis_info)  # type: AxisInfo

    def _get_rotation_quaternion(self) -> Quaternion:
        angle = self.angle if self.counterclockwise_rotation else -self.angle
        rotation_axis_vector = self._get_rotation_axis_vector(self.rotation_axis, self.rotation_axis_direction)
        a = cos(angle / 2)  # type: float
        b = rotation_axis_vector.x * sin(angle / 2)  # type: float
        c = rotation_axis_vector.y * sin(angle / 2)  # type: float
        d = rotation_axis_vector.z * sin(angle / 2)  # type: float
        return Quaternion(a, b, c, d)

    def get_rotation_matrix(self) -> 'Matrix3x3':
        rotation_quaternion = self._get_rotation_quaternion()
        w = rotation_quaternion.w
        x = rotation_quaternion.x
        y = rotation_quaternion.y
        z = rotation_quaternion.z
        return Matrix3x3(
            1-2*(y**2)-2*(z**2), 2*x*y-2*z*w, 2*x*z+2*y*w,
            2*x*y + 2*z*w, 1 - 2*(x**2)-2*(z**2), 2*y*z - 2*x*w,
            2*x*z - 2*y*w, 2*y*z + 2*x*w, 1 - 2*(x**2) - 2*(y**2)
        )

    def _get_rotation_axis_vector(self, rotation_axis: Axis, rotation_axis_direction: AxisDirection) -> Vector3d:
        if rotation_axis == Axis.X:
            return Vector3d(x=1.0 if rotation_axis_direction == AxisDirection.INCREASING_VALUES else -1.0, y=0.0, z=0.0)
        elif rotation_axis == Axis.Y:
            return Vector3d(x=0.0, y=1.0 if rotation_axis_direction == AxisDirection.INCREASING_VALUES else -1.0, z=0.0)
        elif rotation_axis == Axis.Z:
            return Vector3d(x=0.0, y=0.0, z=1.0 if rotation_axis_direction == AxisDirection.INCREASING_VALUES else -1.0)
