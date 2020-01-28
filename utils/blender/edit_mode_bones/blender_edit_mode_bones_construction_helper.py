from typing import Tuple

from ....utils.model_spaces_integration.quaternion import Quaternion
from ....utils.model_spaces_integration.vector3d import Vector3d
from ....utils.model_spaces_integration.model_spaces_info import ModelSpacesInfo
from ....utils.blender.edit_mode_bones.blender_edit_mode_bone import BlenderEditModeBone
from ....utils.model_spaces_integration.vector3d_basing_model_vector3d_builder import Vector3dBasingModelVector3dBuilder


class BlenderEditModeBonesConstructionHelper:
    def calculate_head_and_tail_position(
            self,
            position: 'Vector3d',
            rotation: 'Quaternion',
            scale: 'Vector3d'
    ) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        # Let's assume first that position given is in the middle of bone's length, in the half-way from tail to bone
        # and vice versa

        # Let's assume that bone with no applied rotation to it (that means 0, 0, 0)
        # will be staying vertical with head on the top
        working_bone = BlenderEditModeBone(
            head_position=
            Vector3dBasingModelVector3dBuilder(axis_info=ModelSpacesInfo.BLENDER_AXIS_INFO)
            .forward_axis_value(value=0.0, forward_increasing=True)
            .side_right_value(value=0.0, side_right_increasing=True)
            .up_axis_value(value=0.0, up_increasing=True)
            .build(),
            tail_position=Vector3dBasingModelVector3dBuilder(axis_info=ModelSpacesInfo.BLENDER_AXIS_INFO)
            .forward_axis_value(value=0.10, forward_increasing=True)
            .side_right_value(value=0.0, side_right_increasing=True)
            .up_axis_value(value=0.0, up_increasing=True)
            .build(),
        )
        working_bone.position_using_bone_head_position(position)
        working_bone.scale_as_if_inside_bounding_box(scale)
        working_bone.rotate(rotation)

        head_position = working_bone.head_position.x, working_bone.head_position.y, working_bone.head_position.z
        tail_position = working_bone.tail_position.x, working_bone.tail_position.y, working_bone.tail_position.z

        return head_position, tail_position
