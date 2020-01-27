import copy
from typing import Dict

from ....model.objects.constructing.armature.armature_bind_pose_model_constructor import ArmatureBindPoseModelConstructor
from ....model.objects.model.export_objects_library_model_description.armature_bind_pose_model import ArmatureBindPoseModel
from ....model.objects.model.animated_export_object_model import AnimatedExportObjectModel
from ....utils.model_spaces_integration.axis_info import AxisInfo
from ....model.objects.model.export_objects_library_model_description.armature_hierarchy_model import\
    ArmatureHierarchyModel


class ExportObjectsLibraryModel:
    def __init__(self):
        self.armature_hierarchy = ArmatureHierarchyModel()
        self.animated_export_objects = dict()  # type: Dict[str, AnimatedExportObjectModel]

    def translate_to_space_model(
            self, base_space_model: AxisInfo, target_space_model: AxisInfo):
        result = ExportObjectsLibraryModel()
        result.armature_hierarchy = copy.deepcopy(self.armature_hierarchy)
        result.animated_export_objects = \
            {animated_export_object_name:
                self.animated_export_objects[animated_export_object_name].translate_to_space_model(
                    base_space_model=base_space_model, target_space_model=target_space_model
                )
             for animated_export_object_name in self.animated_export_objects}
        return result

    def reform_for_blender_building_process(self):
        self._check_one_channel_to_one_mesh_assumption()
        return copy.deepcopy(self)

    def _check_one_channel_to_one_mesh_assumption(self):
        channel_meshes_count_dict = dict()  # type: Dict[str, int]
        for channel_node_iter in self.armature_hierarchy.iterate_nodes():
            channel_name = channel_node_iter.node.bone_name
            channel_meshes_count_dict[channel_name] = 0
            for anim_export_object_name in self.animated_export_objects:
                anim_export_object = self.animated_export_objects[anim_export_object_name]
                if channel_name in anim_export_object.bind_bone_poses or \
                        channel_name in anim_export_object.mesh_geometry.bones_weights:
                    channel_meshes_count_dict[channel_name] += 1
        for channel_name in channel_meshes_count_dict:
            if channel_meshes_count_dict[channel_name] > 1:
                raise ValueError("One channel to one mesh assumption is not satisfied!")

    def get_armature_bind_pose_model(self) -> ArmatureBindPoseModel:
        armature_bind_pose_model_constructor = ArmatureBindPoseModelConstructor()
        return armature_bind_pose_model_constructor.construct(self.armature_hierarchy, self.animated_export_objects)
