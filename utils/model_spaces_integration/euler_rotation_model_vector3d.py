import copy
from typing import Tuple

from ...utils.model_spaces_integration.euler_plane import EulerPlane
from ...utils.model_spaces_integration.in_plane_euler_rotation import InPlaneEulerRotation
from ...utils.model_spaces_integration.model_vector3d import ModelVector3d


class EulerRotationModelVector3d:
    def __init__(self, model_vector3d: ModelVector3d):
        self.model_vector3d = copy.deepcopy(model_vector3d)  # type: ModelVector3d

    def get_in_plane_rotations(self) -> Tuple[InPlaneEulerRotation, InPlaneEulerRotation, InPlaneEulerRotation]:
        up_plane = EulerPlane(axis_a=self.model_vector3d.get_forward_axis(),
                              axis_b=self.model_vector3d.get_side_axis())
        forward_plane = EulerPlane(axis_a=self.model_vector3d.get_up_axis(),
                                   axis_b=self.model_vector3d.get_side_axis())
        side_plane = EulerPlane(axis_a=self.model_vector3d.get_up_axis(),
                                axis_b=self.model_vector3d.get_forward_axis())
        in_up_plane_euler_rotation = InPlaneEulerRotation(
            rotation_plane=up_plane,
            rotation_axis=self.model_vector3d.get_up_axis(),
            rotation_axis_direction=self.model_vector3d.get_up_axis_direction(),
            angle=self.model_vector3d.get_up_axis_value(),
            counterclockwise_rotation=True,
            axis_info=self.model_vector3d.axis_info
        )
        in_forward_plane_euler_rotation = InPlaneEulerRotation(
            rotation_plane=forward_plane,
            rotation_axis=self.model_vector3d.get_forward_axis(),
            rotation_axis_direction=self.model_vector3d.get_forward_axis_direction(),
            angle=self.model_vector3d.get_forward_axis_value(),
            counterclockwise_rotation=True,
            axis_info=self.model_vector3d.axis_info
        )
        in_side_plane_euler_rotation = InPlaneEulerRotation(
            rotation_plane=side_plane,
            rotation_axis=self.model_vector3d.get_side_axis(),
            rotation_axis_direction=self.model_vector3d.get_side_axis_right_direction(),
            angle=self.model_vector3d.get_side_axis_value(),
            counterclockwise_rotation=True,
            axis_info=self.model_vector3d.axis_info
        )
        return in_forward_plane_euler_rotation, in_up_plane_euler_rotation, in_side_plane_euler_rotation
