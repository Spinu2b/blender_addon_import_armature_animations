from ....model.objects.constructing.export_objects_library_model_builder import ExportObjectsLibraryModelBuilder
from ....model.objects.model.export_objects_library_model import ExportObjectsLibraryModel


class ExportObjectsLibraryModelConstructor:
    def construct_from_json(self, json_dict) -> ExportObjectsLibraryModel:
        result_builder = ExportObjectsLibraryModelBuilder()
        result_builder.set_armature_hierarchy_model(json_dict["armatureHierarchy"])
        for animated_export_object_model_name in json_dict["animatedExportObjects"]:
            animated_export_object_model_json_dict = \
                json_dict["animatedExportObjects"][animated_export_object_model_name]
            result_builder.add_animated_export_object_model(animated_export_object_model_json_dict)
        return result_builder.build()
