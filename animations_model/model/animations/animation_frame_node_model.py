from typing import List


class AnimationFrameNodeModel:
    def __init__(self, node_name : str,
                 position_x: float,
                 position_y: float,
                 position_z: float,
                 local_position_x: float,
                 local_position_y: float,
                 local_position_z: float,
                 rotation_x: float,
                 rotation_y: float,
                 rotation_z: float,
                 local_rotation_x: float,
                 local_rotation_y: float,
                 local_rotation_z: float,
                 scale_x: float,
                 scale_y: float,
                 scale_z: float,
                 local_scale_x: float,
                 local_scale_y: float,
                 local_scale_z: float):
        self.node_name = node_name  # type: str
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
        self.nodes = []  # type: List[AnimationFrameNodeModel]
