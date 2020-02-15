from model.objects.json_parsing.animated_export_object_model_json_deserializer import \
    AnimatedExportObjectModelJsonDeserializer
from model.objects.json_parsing.export_objects_library_model_parsing.armature_hierarchy_model_json_deserializer import \
    ArmatureHierarchyModelJsonDeserializer
from utils.json_parsing.dict_json_deserializer import DictJsonDeserializer
from utils.json_parsing.json_deserializer import JsonDeserializer
from utils.json_parsing.string_json_deserializer import StringJsonDeserializer


class ExportObjectsLibraryModelJsonDeserializer(JsonDeserializer):
    ATTRIBUTE = {
        "armatureHierarchy": ("armature_hierarchy", ArmatureHierarchyModelJsonDeserializer),
        "animatedExportObjects": ("animated_export_objects",
                                  DictJsonDeserializer[StringJsonDeserializer,
                                                       AnimatedExportObjectModelJsonDeserializer])
    }
