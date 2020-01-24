from .....utils.model_spaces_integration.quaternion import Quaternion
from .....utils.model_spaces_integration.vector3d import Vector3d
from .....utils.model.tree_hierarchy import TreeHierarchy


class ArmatureBindPoseModelNode:
    def __init__(self, position: Vector3d, rotation: Quaternion, scale: Vector3d):
        self.position = position  # type: Vector3d
        self.rotation = rotation  # type: Quaternion
        self.scale = scale  # type: Vector3d


class ArmatureBindPoseModel(TreeHierarchy):
    pass
