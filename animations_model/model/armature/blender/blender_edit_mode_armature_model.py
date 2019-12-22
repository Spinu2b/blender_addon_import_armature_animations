from typing import Generator

from .....animations_model.model.armature.blender.blender_edit_mode_armature_node_model import \
    BlenderEditModeArmatureNodeModel
from .....utils.model.tree_hierarchy import TreeHierarchy


class BlenderChildParentBonePair:
    def __init__(self, child: BlenderEditModeArmatureNodeModel, parent: BlenderEditModeArmatureNodeModel):
        self.child = child  # type: BlenderEditModeArmatureNodeModel
        self.parent = parent  # type: BlenderEditModeArmatureNodeModel


class BlenderEditModeArmatureModel(TreeHierarchy):
    def iterate_all_child_parent_pairs(self) -> Generator[BlenderChildParentBonePair]:
        for node_iter in self.iterate_nodes():
            yield BlenderChildParentBonePair(child=node_iter.node, parent=node_iter.parent)
