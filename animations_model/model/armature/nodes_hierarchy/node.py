from typing import TYPE_CHECKING
from .....utils.model_spaces_integration.model_vector3d import ModelVector3d

if TYPE_CHECKING:
    from .....utils.model_spaces_integration.axis_info import AxisInfo


class Node:
    def __init__(self, name: str,
                 position_x: float=0.0,
                 position_y: float=0.0,
                 position_z: float=0.0,
                 local_position_x: float=0.0,
                 local_position_y: float=0.0,
                 local_position_z: float=0.0,
                 rotation_x: float=0.0,
                 rotation_y: float=0.0,
                 rotation_z: float=0.0,
                 local_rotation_x: float=0.0,
                 local_rotation_y: float=0.0,
                 local_rotation_z: float=0.0,
                 scale_x: float=1.0,
                 scale_y: float=1.0,
                 scale_z: float=1.0,
                 local_scale_x: float=1.0,
                 local_scale_y: float=1.0,
                 local_scale_z: float=1.0
                 ):
        self.name = name  # type: str
        self.position_x = position_x  # type: float
        self.position_y = position_y  # type: float
        self.position_z = position_z  # type: float
        self.local_position_x = local_position_x  # type: float
        self.local_position_y = local_position_y  # type: float
        self.local_position_z = local_position_z  # type: float
        self.rotation_x = rotation_x  # type: float
        self.rotation_y = rotation_y  # type: float
        self.rotation_z = rotation_z  # type: float
        self.local_rotation_x = local_rotation_x  # type: float
        self.local_rotation_y = local_rotation_y  # type: float
        self.local_rotation_z = local_rotation_z  # type: float
        self.scale_x = scale_x  # type: float
        self.scale_y = scale_y  # type: float
        self.scale_z = scale_z  # type: float
        self.local_scale_x = local_scale_x  # type: float
        self.local_scale_y = local_scale_y  # type: float
        self.local_scale_z = local_scale_z  # type: float

    def assign_from(self, other_node):
        self.name = other_node.name
        self.position_x = other_node.position_x  # type: float
        self.position_y = other_node.position_y  # type: float
        self.position_z = other_node.position_z  # type: float
        self.local_position_x = other_node.local_position_x  # type: float
        self.local_position_y = other_node.local_position_y  # type: float
        self.local_position_z = other_node.local_position_z  # type: float
        self.rotation_x = other_node.rotation_x  # type: float
        self.rotation_y = other_node.rotation_y  # type: float
        self.rotation_z = other_node.rotation_z  # type: float
        self.local_rotation_x = other_node.local_rotation_x  # type: float
        self.local_rotation_y = other_node.local_rotation_y  # type: float
        self.local_rotation_z = other_node.local_rotation_z  # type: float
        self.scale_x = other_node.scale_x  # type: float
        self.scale_y = other_node.scale_y  # type: float
        self.scale_z = other_node.scale_z  # type: float
        self.local_scale_x = other_node.local_scale_x  # type: float
        self.local_scale_y = other_node.local_scale_y  # type: float
        self.local_scale_z = other_node.local_scale_z  # type: float

    def translate_to_space_model(self, base_space_model: 'AxisInfo', target_space_model: 'AxisInfo'):
        position_model_vector3d = ModelVector3d(
            axis_info=base_space_model, x=self.position_x, y=self.position_y, z=self.position_z) \
            .translate_to_model_axis(target_axis_info=target_space_model)
        rotation_model_vector3d = ModelVector3d(
            axis_info=base_space_model, x=self.rotation_x, y=self.rotation_y, z=self.rotation_z
        ).translate_to_model_axis(target_axis_info=target_space_model)
        scale_model_vector3d = ModelVector3d(
            axis_info=base_space_model, x=self.scale_x, y=self.scale_y, z=self.scale_z
        ).translate_to_model_axis(target_axis_info=target_space_model)
        local_position_model_vector3d = ModelVector3d(
            axis_info=base_space_model, x=self.local_position_x, y=self.local_position_y, z=self.local_position_z
        ).translate_to_model_axis(target_axis_info=target_space_model)
        local_rotation_model_vector3d = ModelVector3d(
            axis_info=base_space_model, x=self.local_rotation_x, y=self.local_rotation_y, z=self.local_rotation_z
        ).translate_to_model_axis(target_axis_info=target_space_model)
        local_scale_model_vector3d = ModelVector3d(
            axis_info=base_space_model, x=self.local_scale_x, y=self.local_scale_y, z=self.local_scale_z
        ).translate_to_model_axis(target_axis_info=target_space_model)

        return Node(
            name=self.name,
            position_x=position_model_vector3d.x,
            position_y=position_model_vector3d.y,
            position_z=position_model_vector3d.z,
            local_position_x=local_position_model_vector3d.x,
            local_position_y=local_position_model_vector3d.y,
            local_position_z=local_position_model_vector3d.z,
            rotation_x=rotation_model_vector3d.x,
            rotation_y=rotation_model_vector3d.y,
            rotation_z=rotation_model_vector3d.z,
            local_rotation_x=local_rotation_model_vector3d.x,
            local_rotation_y=local_rotation_model_vector3d.y,
            local_rotation_z=local_rotation_model_vector3d.z,
            scale_x=scale_model_vector3d.x,
            scale_y=scale_model_vector3d.y,
            scale_z=scale_model_vector3d.z,
            local_scale_x=local_scale_model_vector3d.x,
            local_scale_y=local_scale_model_vector3d.y,
            local_scale_z=local_scale_model_vector3d.z
        )

    def set_local_offsets_to_home_values(self):
        return Node(
            name=self.name,
            position_x=self.position_x,
            position_y=self.position_y,
            position_z=self.position_z,
            local_position_x=0.0,
            local_position_y=0.0,
            local_position_z=0.0,
            rotation_x=self.rotation_x,
            rotation_y=self.rotation_y,
            rotation_z=self.rotation_z,
            local_rotation_x=0.0,
            local_rotation_y=0.0,
            local_rotation_z=0.0,
            scale_x=self.scale_x,
            scale_y=self.scale_y,
            scale_z=self.scale_z,
            local_scale_x=1.0,
            local_scale_y=1.0,
            local_scale_z=1.0
        )
