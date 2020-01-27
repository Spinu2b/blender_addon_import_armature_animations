from typing import Dict, Optional

from .....utils.model_spaces_integration.quaternion import Quaternion
from .....utils.model_spaces_integration.vector3d import Vector3d
from .....model.objects.model.animated_export_object_model import AnimatedExportObjectModel
from .....model.objects.model.animated_export_object_model_description.bone_bind_pose import BoneBindPose
from .....model.objects.model.export_objects_library_model_description.armature_bind_pose_model import\
    ArmatureBindPoseModel, \
    ArmatureBindPoseModelNode
from .....model.objects.model.export_objects_library_model_description.armature_hierarchy_model import\
    ArmatureHierarchyModel


class ArmatureBindPoseModelConstructor:
    def construct(self, armature_hierarchy_model: ArmatureHierarchyModel,
                  animated_export_objects: Dict[str, AnimatedExportObjectModel]) -> ArmatureBindPoseModel:
        result = ArmatureBindPoseModel()
        bone_bind_poses_overall_dict = {bone_iter.node.bone_name:
                                        self._find_bone_bind_pose(animated_export_objects, bone_iter.node.bone_name)
                                        for bone_iter in armature_hierarchy_model.iterate_nodes()}
        bone_bind_poses_overall_dict = {bone_name: bone_bind_poses_overall_dict[bone_name] for bone_name in
                                        bone_bind_poses_overall_dict if bone_bind_poses_overall_dict[bone_name]
                                        is not None}
        bone_bind_pose_armature_model_building_nodes_dict = {
            bone_name:
            ArmatureBindPoseModelNode(bone_name=bone_name,
                                      position=bone_bind_poses_overall_dict[bone_name].position,
                                      rotation=bone_bind_poses_overall_dict[bone_name].rotation,
                                      scale=bone_bind_poses_overall_dict[bone_name].scale)
            for bone_name in bone_bind_poses_overall_dict}

        for bone_iter in armature_hierarchy_model.iterate_nodes():
            bone_key = bone_iter.key
            bone_parent_key = bone_iter.parent_key
            if bone_key in bone_bind_pose_armature_model_building_nodes_dict:
                result.add_node(parent_key=bone_parent_key, node_key=bone_key,
                                node=bone_bind_pose_armature_model_building_nodes_dict[bone_key])
            else:
                result.add_node(
                    parent_key=bone_parent_key, node_key=bone_key,
                    node=ArmatureBindPoseModelNode(
                        bone_name=bone_key,
                        position=Vector3d(0.0, 0.0, 0.0),
                        rotation=Quaternion(1.0, 0.0, 0.0),
                        scale=Vector3d(1.0, 1.0, 1.0)
                    ))
        return result

    def _find_bone_bind_pose(
            self,
            animated_export_objects: Dict[str, AnimatedExportObjectModel],
            bone_name: str) -> Optional[BoneBindPose]:
        for anim_export_obj_name in animated_export_objects:
            anim_export_obj = animated_export_objects[anim_export_obj_name]
            if bone_name in anim_export_obj.bind_bone_poses:
                return anim_export_obj.bind_bone_poses[bone_name]
        return None
