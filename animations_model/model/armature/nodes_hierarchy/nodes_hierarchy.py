import copy
from typing import List
from typing import TYPE_CHECKING

from .....utils.model.tree_hierarchy import TreeHierarchy

if TYPE_CHECKING:
    from .....utils.model_spaces_integration.axis_info import AxisInfo


class NodesHierarchy(TreeHierarchy):
    def translate_to_space_model(self, base_space_model: 'AxisInfo', target_space_model: 'AxisInfo'):
        result = copy.deepcopy(self)
        for node_iter in result.iterate_nodes():
            node_iter.node.assign_from(node_iter.node.translate_to_space_model(
                base_space_model=base_space_model,
                target_space_model=target_space_model
            ))
        return result

    def set_local_offsets_to_home_values(self):
        result = copy.deepcopy(self)
        for node_iter in result.iterate_nodes():
            node_iter.node.assign_from(node_iter.node.set_local_offsets_to_home_values())
        return result

    def get_nodes_names(self) -> List[str]:
        return list(set([node_iter.node.name for node_iter in self.iterate_nodes()]))
