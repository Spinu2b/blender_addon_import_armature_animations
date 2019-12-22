from typing import List, Generator, Optional

from ....animations_model.constructing.deriving_unified_armature.animation_frame_model_to_nodes_hierarchy_converter\
    import AnimationFrameModelToNodesHierarchyConverter
from ....animations_model.model.animations.animation_frame_node_model import AnimationFrameNodeModel
from ....animations_model.model.armature.nodes_hierarchy.nodes_hierarchy import NodesHierarchy


class AnimationFrameModelNodeIter:
    def __init__(self, parent: AnimationFrameNodeModel, animation_frame_node_model: AnimationFrameNodeModel):
        self.parent = parent  # type: AnimationFrameNodeModel
        self.animation_frame_node_model = animation_frame_node_model  # type: AnimationFrameNodeModel


class AnimationFrameModel:
    def __init__(self):
        self.nodes = []  # type: List[AnimationFrameNodeModel]

    def get_nodes_hierarchy(self) -> NodesHierarchy:
        return AnimationFrameModelToNodesHierarchyConverter().convert(self)

    def iterate_nodes(self,) -> Generator[AnimationFrameModelNodeIter]:
        for node in self.nodes:
            yield from self._traverse_nodes_hierarchy(parent=None, node=node)

    def _traverse_nodes_hierarchy(self, parent: Optional[AnimationFrameNodeModel], node: AnimationFrameNodeModel)\
            -> Generator[AnimationFrameModelNodeIter]:
        yield AnimationFrameModelNodeIter(parent=parent, animation_frame_node_model=node)
        for child_node in node.nodes:
            yield from self._traverse_nodes_hierarchy(parent=node, node=child_node)
