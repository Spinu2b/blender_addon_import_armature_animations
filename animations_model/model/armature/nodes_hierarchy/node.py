from typing import List


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
        self.children = []  # type: List[Node]
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
