import copy
from typing import Optional, List

from ..utils.model_spaces_integration.quaternion import Quaternion
from ..utils.model_spaces_integration.quaternion_math_helper import QuaternionMathHelper
from ..utils.model_spaces_integration.vector3d import Vector3d


class AnimationFrameDictNode:
    def __init__(self,
                 bone_name: str,
                 position: Vector3d,
                 local_position: Vector3d,
                 rotation: Quaternion,
                 local_rotation: Quaternion,
                 scale: Vector3d,
                 local_scale: Vector3d):
        self.bone_name = bone_name  # type: str
        self.position = copy.deepcopy(position)  # type: Vector3d
        self.local_position = copy.deepcopy(local_position)  # type: Vector3d
        self.rotation = copy.deepcopy(rotation)  # type: Quaternion
        self.local_rotation = copy.deepcopy(local_rotation)  # type: Quaternion
        self.scale = copy.deepcopy(scale)  # type: Vector3d
        self.local_scale = copy.deepcopy(local_scale)  # type: Vector3d
        self.children = []

    def traverse_and_add_node(self, parent_name: Optional[str], node_to_add) -> bool:
        if parent_name == self.bone_name:
            self.children.append(node_to_add)
            return True

        for node in self.children:
            if node.traverse_and_add_node(parent_name=parent_name, node_to_add=node_to_add):
                return True
        return False

    def to_dictionary(self):
        result = dict()
        result["bone_name"] = self.bone_name
        result["positionX"] = self.position.x
        result["positionY"] = self.position.y
        result["positionZ"] = self.position.z
        result["localPositionX"] = self.local_position.x
        result["localPositionY"] = self.local_position.y
        result["localPositionZ"] = self.local_position.z
        result["rotationW"] = self.rotation.w
        result["rotationX"] = self.rotation.x
        result["rotationY"] = self.rotation.y
        result["rotationZ"] = self.rotation.z
        result["localRotationW"] = self.local_rotation.w
        result["localRotationX"] = self.local_rotation.x
        result["localRotationY"] = self.local_rotation.y
        result["localRotationZ"] = self.local_rotation.z
        result["scaleX"] = self.scale.x
        result["scaleY"] = self.scale.y
        result["scaleZ"] = self.scale.z
        result["localScaleX"] = self.local_scale.x
        result["localScaleY"] = self.local_scale.y
        result["localScaleZ"] = self.local_scale.z
        result["children"] = self._get_children_list()

    def _get_children_list(self):
        return [node.to_dictionary() for node in self.children]


class AnimationFrameDictModel:
    def __init__(self):
        self.nodes = []  # type: List[AnimationFrameDictNode]

    def add_node(self,
                 parent_name: Optional[str],
                 bone_name: str,
                 position: Vector3d,
                 local_position: Vector3d,
                 rotation: Quaternion,
                 local_rotation: Quaternion,
                 scale: Vector3d,
                 local_scale: Vector3d):
        node = AnimationFrameDictNode(
            bone_name=bone_name,
            position=position,
            local_position=local_position,
            rotation=rotation,
            local_rotation=local_rotation,
            scale=scale,
            local_scale=local_scale
        )

        self._traverse_and_add_node(parent_name=parent_name, node_to_add=node)

    def _traverse_and_add_node(self, parent_name: Optional[str], node_to_add: AnimationFrameDictNode):
        if parent_name is None:
            self.nodes.append(node_to_add)

        for node in self.nodes:
            if node.traverse_and_add_node(parent_name=parent_name, node_to_add=node_to_add):
                return
        raise Exception("Could not find parent of that name: {}".format(parent_name))

    def to_dictionary(self):
        result = dict()
        result["nodes"] = self._get_nodes_list()
        return result

    def _get_nodes_list(self):
        return [node.to_dictionary() for node in self.nodes]


class AnimationFrameDictBuilder:
    def __init__(self):
        self.result = AnimationFrameDictModel()

    def add_node(self,
                 parent_name: Optional[str],
                 name: str,
                 position: Vector3d = Vector3d(0.0, 0.0, 0.0),
                 local_position: Vector3d = Vector3d(0.0, 0.0, 0.0),
                 rotation: Quaternion = QuaternionMathHelper.get_zero_relative_rotation_quaternion(),
                 local_rotation: Quaternion = QuaternionMathHelper.get_zero_relative_rotation_quaternion(),
                 scale: Vector3d = Vector3d(1.0, 1.0, 1.0),
                 local_scale: Vector3d = Vector3d(1.0, 1.0, 1.0)):
        self.result.add_node(
            parent_name=parent_name,
            bone_name=name,
            position=position,
            local_position=local_position,
            rotation=rotation,
            local_rotation=local_rotation,
            scale=scale,
            local_scale=local_scale
        )

    def build(self):
        return self.result.to_dictionary()
