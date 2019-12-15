from animations_model.constructing.building_blender_edit_mode_armature.\
    unified_armature_model_to_blender_edit_mode_armature_model_converter import \
    UnifiedArmatureModelToBlenderEditModeArmatureModelConverter
from animations_model.model.armature.blender.blender_edit_mode_armature_model import BlenderEditModeArmatureModel
from animations_model.model.armature.nodes_hierarchy.nodes_hierarchy import NodesHierarchy


class UnifiedArmatureModel:
    def __init__(self, nodes_hierarchy: NodesHierarchy):
        self.nodes_hierarchy = nodes_hierarchy  # type: NodesHierarchy

    def get_blender_edit_mode_armature_model(self) -> BlenderEditModeArmatureModel:
        return UnifiedArmatureModelToBlenderEditModeArmatureModelConverter().convert(self)
