from typing import Dict, Tuple, List

from ....model.objects.model.animated_export_object_model_description.materials_description.material import Material
from ....model.objects.model.animated_export_object_model_description.materials_description.texture import Texture, Color
from ....utils.model_spaces_integration.vector2d import Vector2d
from ....model.objects.model.animated_export_object_model import AnimatedExportObjectModel
from ....model.objects.model.animated_export_object_model_description.bone_bind_pose import BoneBindPose
from ....model.objects.model.animated_export_object_model_description.mesh_geometry import MeshGeometry
from ....model.objects.model.animated_export_object_model_description.transform_model import TransformModel
from ....utils.model_spaces_integration.quaternion import Quaternion
from ....utils.model_spaces_integration.vector3d import Vector3d


class TextureModelBuilder:
    def from_json_dict(self, texture_json_dict) -> Texture:
        result = Texture()
        result.pixels = [Color(p["red"], p["green"], p["blue"], p["alpha"]) for p in texture_json_dict["pixels"]]
        result.width = texture_json_dict["width"]
        result.height = texture_json_dict["height"]
        result.name = texture_json_dict["name"]
        return result


class MaterialModelBuilder:
    def from_json_dict(self, material_json_dict) -> Material:
        result = Material()
        result.main_texture = TextureModelBuilder().from_json_dict(material_json_dict["mainTexture"])
        result.main_texture_offset = Vector2d.from_json_dict(material_json_dict["mainTextureOffset"])
        result.main_texture_scale = Vector2d.from_json_dict(material_json_dict["mainTextureScale"])
        result.name = material_json_dict["name"]
        return result


class AnimatedExportObjectModelBuilder:
    def from_json(self, animated_export_object_model_json_dict) -> AnimatedExportObjectModel:
        result = AnimatedExportObjectModel()
        result.transform_model = self._get_transform_model(animated_export_object_model_json_dict["transform"])
        result.mesh_geometry = self._get_mesh_geometry(animated_export_object_model_json_dict["meshGeometry"])
        result.bind_bone_poses = self._get_bind_bone_poses(animated_export_object_model_json_dict["bindBonePoses"])
        result.name = animated_export_object_model_json_dict["Name"]
        result.materials = self._get_materials(animated_export_object_model_json_dict["materials"])
        return result

    def _get_transform_model(self, transform_json_dict) -> TransformModel:
        result = TransformModel()
        result.position = Vector3d.from_json_dict(transform_json_dict["position"])
        result.rotation = Quaternion.from_json_dict(transform_json_dict["rotation"])
        result.scale = Vector3d.from_json_dict(transform_json_dict["scale"])
        result.local_position = Vector3d.from_json_dict(transform_json_dict["localPosition"])
        result.local_rotation = Quaternion.from_json_dict(transform_json_dict["localRotation"])
        result.local_scale = Vector3d.from_json_dict(transform_json_dict["localScale"])
        return result

    def _get_mesh_geometry(self, mesh_geometry_json_dict) -> MeshGeometry:
        result = MeshGeometry()
        result.vertices = [Vector3d.from_json_dict(x) for x in mesh_geometry_json_dict["vertices"]]
        result.triangles = [self._triangle_definition_from_json_dict(x) for x in mesh_geometry_json_dict["triangles"]]
        result.bones_weights = {bone_weights_bone_name: self._get_bone_weights_dict(
            mesh_geometry_json_dict["bonesWeights"][bone_weights_bone_name]) for bone_weights_bone_name in
            mesh_geometry_json_dict["bonesWeights"]}
        result.normals = [Vector3d.from_json_dict(x) for x in mesh_geometry_json_dict["normals"]]
        result.uv_maps = [[Vector2d.from_json_dict(x) for x in uv] for uv in mesh_geometry_json_dict["uvMaps"]]
        return result

    def _get_bind_bone_poses(self, bind_bone_poses_json_dict) -> Dict[str, BoneBindPose]:
        return {bone_name: self._get_bone_bind_pose_from_json_dict(bind_bone_poses_json_dict[bone_name])
                for bone_name in bind_bone_poses_json_dict}

    def _triangle_definition_from_json_dict(self, triangle_csharp_tuple_json_dict) -> Tuple[int, int, int]:
        return (triangle_csharp_tuple_json_dict["Item1"], triangle_csharp_tuple_json_dict["Item2"],
                triangle_csharp_tuple_json_dict["Item3"])

    def _get_bone_weights_dict(self, bone_weights_json_dict) -> Dict[int, float]:
        return {int(x): float(bone_weights_json_dict[x]) for x in bone_weights_json_dict}

    def _get_bone_bind_pose_from_json_dict(self, bone_bind_pose_json_dict) -> BoneBindPose:
        result = BoneBindPose()
        result.position = Vector3d.from_json_dict(bone_bind_pose_json_dict["position"])
        result.rotation = Quaternion.from_json_dict(bone_bind_pose_json_dict["rotation"])
        result.scale = Vector3d.from_json_dict(bone_bind_pose_json_dict["scale"])
        result.bone_name = bone_bind_pose_json_dict["boneName"]
        return result

    def _get_materials(self, materials_json_list) -> List[Material]:
        result = []  # type: List[Material]
        material_model_builder = MaterialModelBuilder()
        for material_json_dict in materials_json_list:
            result.append(material_model_builder.from_json_dict(material_json_dict))
        return result
