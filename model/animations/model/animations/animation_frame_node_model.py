import copy

from .....utils.model_spaces_integration.quaternion import Quaternion
from .....utils.model_spaces_integration.vector3d import Vector3d


class AnimationFrameNodeModel:
    def __init__(self, node_name : str,
                 position: Vector3d,
                 local_position: Vector3d,
                 rotation: Quaternion,
                 local_rotation: Quaternion,
                 scale: Vector3d,
                 local_scale: Vector3d):
        self.node_name = node_name  # type: str
        self.position = copy.deepcopy(position)  # type: Vector3d
        self.local_position = copy.deepcopy(local_position)  # type: Vector3d
        self.rotation = copy.deepcopy(rotation)  # type: Quaternion
        self.local_rotation = copy.deepcopy(local_rotation)  # type: Quaternion
        self.scale = copy.deepcopy(scale)  # type: Vector3d
        self.local_scale = copy.deepcopy(local_scale)  # type: Vector3d

    @classmethod
    def from_json_dict_tree_building(cls, json_dict):
        return AnimationFrameNodeModel(
            node_name=json_dict["boneName"],
            position=Vector3d.from_json_dict(json_dict["position"]),
            local_position=Vector3d.from_json_dict(json_dict["localPosition"]),
            rotation=Quaternion.from_json_dict(json_dict["rotation"]),
            local_rotation=Quaternion.from_json_dict(json_dict["localRotation"]),
            scale=Vector3d.from_json_dict(json_dict["scale"]),
            local_scale=Vector3d.from_json_dict(json_dict["localScale"])
        )
