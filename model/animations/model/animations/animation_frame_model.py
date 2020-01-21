from typing import TYPE_CHECKING

from utils.model.tree_hierarchy import TreeHierarchy
from ....animations_model.constructing.deriving_unified_armature. \
    animation_frame_model_to_nodes_hierarchy_converter import AnimationFrameModelToNodesHierarchyConverter

if TYPE_CHECKING:
    from ....animations_model.model.armature.nodes_hierarchy.nodes_hierarchy import NodesHierarchy


class AnimationFrameModel(TreeHierarchy):
    def get_nodes_hierarchy(self) -> 'NodesHierarchy':
        return AnimationFrameModelToNodesHierarchyConverter().convert(self)
