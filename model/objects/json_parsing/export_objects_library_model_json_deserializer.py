from model.objects.json_parsing.export_objects_library_model_parsing.armature_hierarchy_model_json_deserializer import \
    ArmatureHierarchyModelJsonDeserializer
from utils.json_parsing.json_deserializer import JsonDeserializer


class ExportObjectsLibraryModelJsonDeserializer(JsonDeserializer):
    ATTRIBUTE = {
        "armatureHierarchy": ("armature_hierarchy", ArmatureHierarchyModelJsonDeserializer),
        "animatedExportObjects": ("animated_export_objects",
                                  DictJsonDeserializer[StringJsonDeserializer,
                                                       AnimatedExportObjectModelJsonDeserializer])
    }
