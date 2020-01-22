from model.objects.constructing.animated_export_object_model_builder import AnimatedExportObjectModelBuilder
from model.objects.model.export_objects_library_model import ExportObjectsLibraryModel
from model.objects.model.export_objects_library_model_description.armature_hierarchy_model import \
    ArmatureHierarchyModel, ArmatureHierarchyModelNode
from utils.model.json_dict_tree_builder import JsonDictTreeBuilder


class ExportObjectsLibraryModelBuilder:
    def __init__(self):
        self.result = ExportObjectsLibraryModel()

    def set_armature_hierarchy_model(self, armature_hierarchy_json_dict):
        self.result.armature_hierarchy = JsonDictTreeBuilder().build_from(
            ArmatureHierarchyModel, ArmatureHierarchyModelNode, armature_hierarchy_json_dict)

    def add_animated_export_object_model(self, animated_export_object_model_json_dict):
        animated_export_object_model = \
            AnimatedExportObjectModelBuilder().from_json(animated_export_object_model_json_dict)
        self.result.animated_export_objects[animated_export_object_model.name] = animated_export_object_model

    def build(self) -> ExportObjectsLibraryModel:
        return self.result
