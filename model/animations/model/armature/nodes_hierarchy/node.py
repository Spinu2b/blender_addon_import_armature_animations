import copy
from typing import TYPE_CHECKING

from .....utils.model_spaces_integration.model_quaternion import ModelQuaternion
from .....utils.model_spaces_integration.quaternion import Quaternion
from .....utils.model_spaces_integration.quaternion_math_helper import QuaternionMathHelper
from .....utils.model_spaces_integration.vector3d import Vector3d
from .....utils.model_spaces_integration.model_vector3d import ModelVector3d

if TYPE_CHECKING:
    from .....utils.model_spaces_integration.axis_info import AxisInfo


class Node:
    def __init__(self, name: str,
                 position: Vector3d=Vector3d(0.0, 0.0, 0.0),
                 local_position: Vector3d=Vector3d(0.0, 0.0, 0.0),
                 rotation: Quaternion=QuaternionMathHelper.get_zero_relative_rotation_quaternion(),
                 local_rotation: Quaternion=QuaternionMathHelper.get_zero_relative_rotation_quaternion(),
                 scale: Vector3d=Vector3d(1.0, 1.0, 1.0),
                 local_scale: Vector3d=Vector3d(1.0, 1.0, 1.0),
                 ):
        self.name = name  # type: str
        self.position = copy.deepcopy(position)  # type: Vector3d
        self.local_position = copy.deepcopy(local_position)  # type: Vector3d
        self.rotation = copy.deepcopy(rotation)  # type: Quaternion
        self.local_rotation = copy.deepcopy(local_rotation)  # type: Quaternion
        self.scale = copy.deepcopy(scale)  # type: Vector3d
        self.local_scale = copy.deepcopy(local_scale)  # type: Vector3d

    def assign_from(self, other_node):
        self.name = other_node.name  # type: str
        self.position = copy.deepcopy(other_node.position)  # type: Vector3d
        self.local_position = copy.deepcopy(other_node.local_position)  # type: Vector3d
        self.rotation = copy.deepcopy(other_node.rotation)  # type: Quaternion
        self.local_rotation = copy.deepcopy(other_node.local_rotation)  # type: Quaternion
        self.scale = copy.deepcopy(other_node.scale)  # type: Vector3d
        self.local_scale = copy.deepcopy(other_node.local_scale)  # type: Vector3d

    def translate_to_space_model(self, base_space_model: 'AxisInfo', target_space_model: 'AxisInfo'):
        position_model_vector3d = ModelVector3d(
            axis_info=base_space_model, x=self.position.x, y=self.position.y, z=self.position.z) \
            .translate_to_model_axis(target_axis_info=target_space_model)
        rotation_model_quaternion = ModelQuaternion(
            axis_info=base_space_model, w=self.rotation.w, x=self.rotation.x, y=self.rotation.y, z=self.rotation.z
        ).translate_to_model_axis(target_axis_info=target_space_model)
        scale_model_vector3d = ModelVector3d(
            axis_info=base_space_model, x=self.scale.x, y=self.scale.y, z=self.scale.z
        ).translate_to_model_axis(target_axis_info=target_space_model)
        local_position_model_vector3d = ModelVector3d(
            axis_info=base_space_model, x=self.local_position.x, y=self.local_position.y, z=self.local_position.z
        ).translate_to_model_axis(target_axis_info=target_space_model)
        local_rotation_model_quaternion = ModelQuaternion(
            axis_info=base_space_model, w=self.local_rotation.w,
            x=self.local_rotation.x, y=self.local_rotation.y, z=self.local_rotation.z
        ).translate_to_model_axis(target_axis_info=target_space_model)
        local_scale_model_vector3d = ModelVector3d(
            axis_info=base_space_model, x=self.local_scale.x, y=self.local_scale.y, z=self.local_scale.z
        ).translate_to_model_axis(target_axis_info=target_space_model)

        return Node(
            name=self.name,
            position=position_model_vector3d.to_vector3d(),
            local_position=local_position_model_vector3d.to_vector3d(),
            rotation=rotation_model_quaternion.to_quaternion(),
            local_rotation=local_rotation_model_quaternion.to_quaternion(),
            scale=scale_model_vector3d.to_vector3d(),
            local_scale=local_scale_model_vector3d.to_vector3d()
        )

    def set_local_offsets_to_home_values(self):
        return Node(
            name=self.name,
            position=self.position,
            local_position=Vector3d(0.0, 0.0, 0.0),
            rotation=self.rotation,
            local_rotation=QuaternionMathHelper.get_zero_relative_rotation_quaternion(),
            scale=self.scale,
            local_scale=Vector3d(1.0, 1.0, 1.0)
        )

    def translate_absolute_offsets_by(self, offsets: Vector3d):
        return Node(
            name=self.name,
            position=self.position + offsets,
            local_position=self.local_position,
            rotation=self.rotation,
            local_rotation=self.local_rotation,
            scale=self.scale,
            local_scale=self.local_scale
        )
