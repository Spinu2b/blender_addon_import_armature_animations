import copy
from typing import TYPE_CHECKING

from ....animations_model.model.armature.nodes_hierarchy.node import Node
from ....animations_model.model.armature.nodes_hierarchy.nodes_hierarchy import NodesHierarchy
from ....utils.model.tree_hierarchy import TreeNodeContainer

if TYPE_CHECKING:
    from ....animations_model.model.animations.animation_frame_model import AnimationFrameModel
    from ....animations_model.model.animations.animation_frame_node_model import AnimationFrameNodeModel


class AnimationFrameModelToNodesHierarchyConverter:
    ROOT_NAME = "ROOT_NODE"

    def convert(self, animation_frame_model: 'AnimationFrameModel') -> NodesHierarchy:
        result = NodesHierarchy()
        result.add_node(parent_name=None, node=Node(name=self.ROOT_NAME))
        for animation_frame_node_iter in animation_frame_model.iterate_nodes():
            result.add_node(
                parent_name=animation_frame_node_iter.parent.node_name if animation_frame_node_iter.parent
                is not None else self.ROOT_NAME,
                node=self._construct_node(animation_frame_node_iter.animation_frame_node_model))
        result = self._recalculate_nodes_offsets_as_root_being_geometrical_center(result)
        return result

    def _construct_node(self, animation_frame_node_model: 'AnimationFrameNodeModel') -> Node:
        return Node(
            name=animation_frame_node_model.node_name,
            position_x=animation_frame_node_model.position_x,
            position_y=animation_frame_node_model.position_y,
            position_z=animation_frame_node_model.position_z,
            local_position_x=animation_frame_node_model.local_position_x,
            local_position_y=animation_frame_node_model.local_position_y,
            local_position_z=animation_frame_node_model.local_position_z,
            rotation_x=animation_frame_node_model.rotation_x,
            rotation_y=animation_frame_node_model.rotation_y,
            rotation_z=animation_frame_node_model.rotation_z,
            local_rotation_x=animation_frame_node_model.local_rotation_x,
            local_rotation_y=animation_frame_node_model.local_rotation_y,
            local_rotation_z=animation_frame_node_model.local_rotation_z,
            scale_x=animation_frame_node_model.rotation_x,
            scale_y=animation_frame_node_model.rotation_y,
            scale_z=animation_frame_node_model.rotation_z,
            local_scale_x=animation_frame_node_model.local_scale_x,
            local_scale_y=animation_frame_node_model.local_scale_y,
            local_scale_z=animation_frame_node_model.local_scale_z
        )

    def _recalculate_nodes_offsets_as_root_being_geometrical_center(
            self, nodes_hierarchy: NodesHierarchy) -> NodesHierarchy:
        nodes_hierarchy = copy.deepcopy(nodes_hierarchy)
        root = nodes_hierarchy.get_root().node  # type: Node
        average_position_x = 0.0  # type: float
        average_position_y = 0.0  # type: float
        average_position_z = 0.0  # type: float
        nodes_count = 0  # type: int
        for node_iter in nodes_hierarchy.iterate_nodes():
            if node_iter.node.name != root.name:
                average_position_x += node_iter.node.position_x
                average_position_y += node_iter.node.position_y
                average_position_z += node_iter.node.position_z
                nodes_count += 1
        average_position_x /= nodes_count
        average_position_y /= nodes_count
        average_position_z /= nodes_count
        nodes_hierarchy.root.node.position_x = average_position_x
        nodes_hierarchy.root.node.position_y = average_position_y
        nodes_hierarchy.root.node.position_z = average_position_z
        nodes_hierarchy = self._recalculate_root_children_nodes_local_offsets(nodes_hierarchy)
        return nodes_hierarchy

    def _is_close_enough_to_zero(self, value: float) -> bool:
        margin = 0.000001
        return abs(value) < margin

    def _recalculate_root_children_nodes_local_offsets(self, nodes_hierarchy: NodesHierarchy) -> NodesHierarchy:
        nodes_hierarchy = copy.deepcopy(nodes_hierarchy)
        root_container = nodes_hierarchy.get_root()  # type: TreeNodeContainer
        root = root_container.node  # type: Node

        root_first_child = root_container.children[0].node  # type: Node
        old_root_rotation_x = root_first_child.rotation_x - root_first_child.local_rotation_x
        old_root_rotation_y = root_first_child.rotation_y - root_first_child.local_rotation_y
        old_root_rotation_z = root_first_child.rotation_z - root_first_child.local_rotation_z

        old_root_scale_x = root_first_child.scale_x / root_first_child.local_scale_x
        old_root_scale_y = root_first_child.scale_y / root_first_child.local_scale_y
        old_root_scale_z = root_first_child.scale_z / root_first_child.local_scale_z

        for root_child_iter in nodes_hierarchy.root.children:
            root_child = root_child_iter.node
            root_child.local_position_x = root_child.position_x - root.position_x
            root_child.local_position_y = root_child.position_y - root.position_y
            root_child.local_position_z = root_child.position_z - root.position_z

            root_child.local_rotation_x += old_root_rotation_x
            root_child.local_rotation_y += old_root_rotation_y
            root_child.local_rotation_z += old_root_rotation_z

            if not self._is_close_enough_to_zero(old_root_scale_x):
                root_child.local_scale_x /= old_root_scale_x
            else:
                root_child.local_scale_x = 0.0

            if not self._is_close_enough_to_zero(old_root_scale_y):
                root_child.local_scale_y /= old_root_scale_y
            else:
                root_child.local_scale_y = 0.0

            if not self._is_close_enough_to_zero(old_root_scale_z):
                root_child.local_scale_z /= old_root_scale_z
            else:
                root_child.local_scale_z = 0.0

        return nodes_hierarchy
