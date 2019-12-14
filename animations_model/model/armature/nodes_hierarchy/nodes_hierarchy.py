from typing import Optional

from animations_model.model.animations.animation_frame_node_model import AnimationFrameNodeModel
from animations_model.model.armature.nodes_hierarchy.node import Node


class NodesHierarchy:
    def __init__(self):
        self.root = None  # type: Optional[Node]

    def _place_under_root(self, animation_frame_node_model: AnimationFrameNodeModel):
        pass

    def _construct_node(self, animation_frame_node_model: AnimationFrameNodeModel) -> Node:
        pass

    def _traverse_children_recursively_and_put(
            self, parent_name: str, node: Node, animation_frame_node_model: AnimationFrameNodeModel):
        for child_node in node.children:
            if child_node.name == parent_name:
                child_node.children.append(self._construct_node(animation_frame_node_model))
            else:
                self._traverse_children_recursively_and_put(
                    parent_name=parent_name,
                    node=child_node,
                    animation_frame_node_model=animation_frame_node_model)

    def add_node(self, parent_name: Optional[str], animation_frame_node_model: AnimationFrameNodeModel):
        if parent_name is None:
            self._place_under_root(animation_frame_node_model)
        else:
            self._traverse_children_recursively_and_put(
                parent_name=parent_name,
                node=self.root,
                animation_frame_node_model=animation_frame_node_model)
