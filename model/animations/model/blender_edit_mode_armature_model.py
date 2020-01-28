from typing import Iterator

from ....utils.model.tree_hierarchy import TreeHierarchy


class BlenderChildParentBonePair:
    def __init__(self, child: 'BlenderEditModeArmatureNodeModel', parent: 'BlenderEditModeArmatureNodeModel'):
        self.child = child  # type: BlenderEditModeArmatureNodeModel
        self.parent = parent  # type: BlenderEditModeArmatureNodeModel


class BlenderEditModeArmatureNodeModel:
    def __init__(self,
                 name: str,
                 head_position_x: float, head_position_y: float, head_position_z: float,
                 tail_position_x: float, tail_position_y: float, tail_position_z: float):
        self.name = name  # type: str
        self.head_position_x = head_position_x  # type: float
        self.head_position_y = head_position_y  # type: float
        self.head_position_z = head_position_z  # type: float
        self.tail_position_x = tail_position_x  # type: float
        self.tail_position_y = tail_position_y  # type: float
        self.tail_position_z = tail_position_z  # type: float


class BlenderEditModeArmatureModel(TreeHierarchy):
    def iterate_all_child_parent_pairs(self) -> Iterator[BlenderChildParentBonePair]:
        for node_iter in self.iterate_nodes():
            yield BlenderChildParentBonePair(child=node_iter.node, parent=node_iter.parent)
