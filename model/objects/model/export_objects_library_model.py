import copy
from typing import Dict

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
