import copy
from typing import TYPE_CHECKING

from ....utils.model_spaces_integration.quaternion_math_helper import QuaternionMathHelper
from ....utils.model_spaces_integration.math_utils import MathUtils
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
            position=animation_frame_node_model.position,
            local_position=animation_frame_node_model.local_position,
            rotation=animation_frame_node_model.rotation,
            local_rotation=animation_frame_node_model.local_rotation,
            scale=animation_frame_node_model.scale,
            local_scale=animation_frame_node_model.local_scale
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
                average_position_x += node_iter.node.position.x
                average_position_y += node_iter.node.position.y
                average_position_z += node_iter.node.position.z
                nodes_count += 1
        average_position_x /= nodes_count
        average_position_y /= nodes_count
        average_position_z /= nodes_count
        nodes_hierarchy.root.node.position.x = average_position_x
        nodes_hierarchy.root.node.position.y = average_position_y
        nodes_hierarchy.root.node.position.z = average_position_z
        #nodes_hierarchy = self._recalculate_root_children_nodes_local_offsets(nodes_hierarchy)
        return nodes_hierarchy

    def _recalculate_root_children_nodes_local_offsets(self, nodes_hierarchy: NodesHierarchy) -> NodesHierarchy:
        nodes_hierarchy = copy.deepcopy(nodes_hierarchy)
        root_container = nodes_hierarchy.get_root()  # type: TreeNodeContainer
        root = root_container.node  # type: Node

        root_first_child = root_container.children[0].node  # type: Node
        old_root_absolute_rotation = QuaternionMathHelper.subtract_relative_rotation(
            absolute_base=root_first_child.rotation,
            relative_rotation=root_first_child.local_rotation
        )

        old_root_absolute_scale = MathUtils.get_scale_ratio_vector3d(
            root_first_child.scale, root_first_child.local_scale)

        for root_child_iter in nodes_hierarchy.root.children:
            root_child = root_child_iter.node
            root_child.local_position = root_child.position - root.position

            root_child.local_rotation = QuaternionMathHelper.add_absolute_rotation(
                relative_base=root_child.local_rotation,
                absolute_rotation=old_root_absolute_rotation
            )

            root_child.local_scale = MathUtils.get_scale_ratio_vector3d(root_child.local_scale, old_root_absolute_scale)

        return nodes_hierarchy
