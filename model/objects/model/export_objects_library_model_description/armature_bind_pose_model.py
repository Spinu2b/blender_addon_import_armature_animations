import copy

from .....model.objects.constructing.armature.armature_bind_pose_model_to_blender_edit_mode_armature_model_converter import \
    ArmatureBindPoseModelToBlenderEditModeArmatureModelConverter
from .....model.animations.model.armature.blender.blender_edit_mode_armature_model import BlenderEditModeArmatureModel
from .....utils.model_spaces_integration.quaternion import Quaternion
from .....utils.model_spaces_integration.vector3d import Vector3d
from .....utils.model.tree_hierarchy import TreeHierarchy


class ArmatureBindPoseModelNode:
    def __init__(self,
                 bone_name: str,
                 position: Vector3d,
                 rotation: Quaternion,
                 scale: Vector3d):
        self.name = bone_name  # type: str
        self.position = copy.deepcopy(position)  # type: Vector3d
        self.rotation = copy.deepcopy(rotation)  # type: Quaternion
        self.scale = copy.deepcopy(scale)  # type: Vector3d


class ArmatureBindPoseModel(TreeHierarchy):
    def get_blender_edit_mode_armature_model(self) -> BlenderEditModeArmatureModel:
        return ArmatureBindPoseModelToBlenderEditModeArmatureModelConverter().convert(self)
