from model.objects.model.export_objects_library_model_description.armature_hierarchy_model import \
    ArmatureHierarchyModel, ArmatureHierarchyModelNode
from utils.json_parsing.tree_json_deserializer import TreeJsonDeserializer


class ArmatureHierarchyModelJsonDeserializer(TreeJsonDeserializer[ArmatureHierarchyModel, ArmatureHierarchyModelNode]):
    pass
