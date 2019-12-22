import copy

from utils.model.tree_hierarchy import TreeHierarchy
from utils.model_spaces_integration.axis_info import AxisInfo


class NodesHierarchy(TreeHierarchy):
    def translate_to_space_model(self, base_space_model: AxisInfo, target_space_model: AxisInfo):
        result = copy.deepcopy(self)
