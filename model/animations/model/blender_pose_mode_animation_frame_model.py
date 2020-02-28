import copy

from ....utils.model_spaces_integration.quaternion import Quaternion
from ....utils.model_spaces_integration.vector3d import Vector3d
from ....utils.model.tree_hierarchy import TreeHierarchy


class BlenderPoseModeAnimationFrameModelNode:
    def __init__(self, bone_name: str, is_keyframe: bool, position: Vector3d, rotation: Quaternion, scale: Vector3d):
        self.bone_name = bone_name  # type: str
        self.is_keyframe = is_keyframe  # type: bool
        self.position = copy.deepcopy(position)  # type: Vector3d
        self.rotation = copy.deepcopy(rotation)  # type: Quaternion
        self.scale = copy.deepcopy(scale)  # type: Vector3d


class BlenderPoseModeAnimationFrameModel(TreeHierarchy):
    pass
