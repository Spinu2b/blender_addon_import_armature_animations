from .....utils.json_parsing.json_deserializer import JsonDeserializer
from .....model.objects.model.export_objects_library_model_description.armature_hierarchy_model import \
    ArmatureHierarchyModel, ArmatureHierarchyModelNode
from .....utils.json_parsing.string_json_deserializer import StringJsonDeserializer
from .....utils.json_parsing.tree_json_deserializer import TreeJsonDeserializer


class ArmatureHierarchyModelNodeJsonDeserializer(JsonDeserializer):
    ATTRIBUTES = {"boneName": ("bone_name", StringJsonDeserializer)}
    RESULT_CLASS = ArmatureHierarchyModelNode


class ArmatureHierarchyModelJsonDeserializer(TreeJsonDeserializer):
    RESULT_CLASS = ArmatureHierarchyModel
    TREE_NODE_KEY_JSON_DESERIALIZER_CLASS = StringJsonDeserializer
    TREE_NODE_JSON_DESERIALIZER_CLASS = ArmatureHierarchyModelNodeJsonDeserializer
