from .....utils.model.tree_hierarchy import TreeHierarchy


class ArmatureHierarchyModelNode:
    def __init__(self, bone_name: str):
        self.bone_name = bone_name

    @classmethod
    def from_json_dict_tree_building(cls, json_dict):
        return ArmatureHierarchyModelNode(bone_name=json_dict["boneName"])


class ArmatureHierarchyModel(TreeHierarchy):
    pass
