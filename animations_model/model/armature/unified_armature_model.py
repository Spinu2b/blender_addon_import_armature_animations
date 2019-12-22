import copy

from animations_model.constructing.building_blender_edit_mode_armature.\
    unified_armature_model_to_blender_edit_mode_armature_model_converter import \
    UnifiedArmatureModelToBlenderEditModeArmatureModelConverter
from animations_model.model.armature.blender.blender_edit_mode_armature_model import BlenderEditModeArmatureModel
from animations_model.model.armature.nodes_hierarchy.nodes_hierarchy import NodesHierarchy
from utils.model_spaces_integration.axis_info import AxisInfo


class UnifiedArmatureModel:
    def __init__(self, nodes_hierarchy: NodesHierarchy):
        self.nodes_hierarchy = nodes_hierarchy  # type: NodesHierarchy

    def get_blender_edit_mode_armature_model(self, base_space_model: AxisInfo) -> BlenderEditModeArmatureModel:
        return UnifiedArmatureModelToBlenderEditModeArmatureModelConverter().convert(self, base_space_model)

    def translate_to_space_model(self, base_space_model: AxisInfo, target_space_model: AxisInfo):
        result = copy.deepcopy(self)
        result.nodes_hierarchy = result.nodes_hierarchy.translate_to_space_model(
            base_space_model=base_space_model, target_space_model=target_space_model)
        return result

    def set_local_offsets_to_home_values(self):
        result = copy.deepcopy(self)
        result.nodes_hierarchy = result.nodes_hierarchy.set_local_offsets_to_home_values()
        return result
