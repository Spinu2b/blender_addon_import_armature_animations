from typing import Tuple

from utils.blender.edit_mode_bones.blender_edit_mode_bone import BlenderEditModeBone
from utils.model_spaces_integration.axis import Axis
from utils.model_spaces_integration.axis_direction import AxisDirection
from utils.model_spaces_integration.axis_info import AxisInfo
from utils.model_spaces_integration.model_vector3d import ModelVector3d
from utils.model_spaces_integration.vector3d_basing_model_vector3d_builder import Vector3dBasingModelVector3dBuilder


class BlenderEditModeBonesConstructionHelper:
    def calculate_head_and_tail_position(
            self,
            position: ModelVector3d,
            rotation: ModelVector3d,
            scale: ModelVector3d
    ) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        blender_axis_info = AxisInfo(
            forward_axis=Axis.Y,
            up_axis=Axis.Z,
            side_axis=Axis.X,
            right_direction_values=AxisDirection.DECREASING_VALUES,
            forward_direction_values=AxisDirection.DECREASING_VALUES,
            up_direction_values=AxisDirection.INCREASING_VALUES
        )
        # Let's assume first that position given is in the middle of bone's length, in the half-way from tail to bone
        # and vice versa
        bone_center_absolute_position = \
            position.translate_to_model_axis(target_axis_info=blender_axis_info)  # type: ModelVector3d
        bone_absolute_euler_rotation = \
            rotation.translate_to_model_axis(target_axis_info=blender_axis_info)  # type: ModelVector3d
        bone_absolute_scale = \
            scale.translate_to_model_axis(target_axis_info=blender_axis_info)  # type: ModelVector3d

        # Let's assume that bone with no applied rotation to it (that means 0, 0, 0)
        # will be staying vertical with head on the top
        working_bone = BlenderEditModeBone(
            head_position=
            Vector3dBasingModelVector3dBuilder(axis_info=blender_axis_info)
            .forward_axis_value(value=0.0, forward_increasing=True)
            .side_axis_value(value=0.0, side_right_increasing=True)
            .up_axis_value(value=0.5, up_increasing=True)
            .build(),
            tail_position=Vector3dBasingModelVector3dBuilder(axis_info=blender_axis_info)
            .forward_axis_value(value=0.0, forward_increasing=True)
            .side_axis_value(value=0.0, side_right_increasing=True)
            .up_axis_value(value=-0.5, up_increasing=True)
            .build(),
        )
        working_bone.position_using_bone_center(bone_center_absolute_position.to_vector3d())
        working_bone.scale_as_if_inside_bounding_box(bone_absolute_scale.to_vector3d())
        working_bone.rotate_using_euler_angles(bone_absolute_euler_rotation.to_euler_rotation_model_vector3d())

        head_position = working_bone.head_position.x, working_bone.head_position.y, working_bone.head_position.z
        tail_position = working_bone.tail_position.x, working_bone.tail_position.y, working_bone.tail_position.z

        return head_position, tail_position
