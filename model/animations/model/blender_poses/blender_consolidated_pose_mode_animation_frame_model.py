from typing import TYPE_CHECKING, Iterator


if TYPE_CHECKING:
    from ....animations_model.model.armature.nodes_hierarchy.nodes_hierarchy import NodesHierarchy
    from ....utils.model.tree_hierarchy import TreeNodeIter


class BlenderConsolidatedPoseModeAnimationFrameModel:
    def __init__(self, nodes_hierarchy: 'NodesHierarchy'):
        self.nodes_hierarchy = nodes_hierarchy

    def iterate_bones(self) -> Iterator['TreeNodeIter']:
        yield from self.nodes_hierarchy.iterate_nodes()
