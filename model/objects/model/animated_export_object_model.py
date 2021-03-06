import copy
from typing import Dict, List

from ....utils.model_spaces_integration.vector2d import Vector2d
from ....model.objects.model.animated_export_object_model_description.materials_description.material import Material
from ....utils.model_spaces_integration.axis_info import AxisInfo
from ....model.objects.model.animated_export_object_model_description.bone_bind_pose import BoneBindPose
from ....model.objects.model.animated_export_object_model_description.mesh_geometry import MeshGeometry
from ....model.objects.model.animated_export_object_model_description.transform_model import TransformModel


class AnimatedExportObjectModel:
    def __init__(self, name: str=""):
        self.name = name  # type: str
        self.transform = TransformModel()
        self.mesh_geometry = MeshGeometry()
        self.bind_bone_poses = dict()  # type: Dict[str, BoneBindPose]
        self.materials = []  # type: List[Material]

    def translate_to_space_model(self, base_space_model: AxisInfo, target_space_model: AxisInfo):
        self.transform.translate_to_space_model(
            base_space_model=base_space_model, target_space_model=target_space_model)
        self.mesh_geometry.translate_to_space_model(
            base_space_model=base_space_model, target_space_model=target_space_model
        )

        for bone_name in self.bind_bone_poses:
            self.bind_bone_poses[bone_name]. \
                 translate_to_space_model(base_space_model=base_space_model, target_space_model=target_space_model)

    def get_valid_uv_map(self) -> List[Vector2d]:
        return [x for x in self.mesh_geometry.uv_maps if len(x) > 0][0]
