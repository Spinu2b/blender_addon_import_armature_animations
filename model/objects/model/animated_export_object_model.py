from typing import Dict

from model.objects.model.animated_export_object_model_description.bone_bind_pose import BoneBindPose
from model.objects.model.animated_export_object_model_description.mesh_geometry import MeshGeometry
from model.objects.model.animated_export_object_model_description.transform_model import TransformModel


class AnimatedExportObjectModel:
    def __init__(self, name: str=""):
        self.name = name  # type: str
        self.transform = TransformModel()
        self.mesh_geometry = MeshGeometry()
        self.bind_bone_poses = dict()  # type: Dict[str, BoneBindPose]
