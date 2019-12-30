from typing import Optional

from ....utils.model_spaces_integration.quaternion import Quaternion
from ....utils.model_spaces_integration.math_utils import MathUtils
from ....utils.model_spaces_integration.quaternion_math_helper import QuaternionMathHelper
from ....utils.model_spaces_integration.vector3d import Vector3d
from ....animations_model.constructing.deriving_unified_armature.consolidation.node_in_hierarchy_info import \
    NodeInHierarchyInfo
from ....animations_model.constructing.deriving_unified_armature.consolidation.node_in_hierarchy_infos_set import \
    NodeInHierarchyInfosSet
from ....animations_model.model.armature.nodes_hierarchy.node import Node
from ....animations_model.model.armature.nodes_hierarchy.nodes_hierarchy import NodesHierarchy
from ....animations_model.model.blender_poses.blender_consolidated_pose_mode_animation_frame_model import \
    BlenderConsolidatedPoseModeAnimationFrameModel


class BlenderConsolidatedPoseModeAnimationFrameModelBuilder:
    def __init__(self):
        self.result_nodes_hierarchy = NodesHierarchy()
        self.nodes_to_add_set = NodeInHierarchyInfosSet(set())

    def _get_scale(self, scale: Vector3d, reference_scale: Vector3d) -> Vector3d:
        return MathUtils.get_scale_ratio_vector3d(scale, reference_scale)

    def consolidate_and_add_node(self,
                                 parent_name: Optional[str],
                                 parent: Optional[Node],
                                 reference: Node,
                                 node_to_consolidate: Node):
        local_rotation = QuaternionMathHelper.derive_local_quaternion_rotation(
            child_absolute_rotation=node_to_consolidate.rotation,
            parent_absolute_rotation=parent.rotation if parent is not None else node_to_consolidate.rotation
        )
        
        node_to_add = \
            Node(
                name=reference.name,
                position=node_to_consolidate.position,
                local_position=node_to_consolidate.position - reference.position,
                rotation=node_to_consolidate.rotation,
                local_rotation=local_rotation,
                scale=node_to_consolidate.scale,
                local_scale=self._get_scale(node_to_consolidate.scale, reference.scale),
            )

        self.nodes_to_add_set.node_in_hierarchy_infos_set.add(
            NodeInHierarchyInfo(node=node_to_add, parent_name=parent_name))

    def consolidate_non_present_bone_and_add_node(self,
                                                  parent_name: Optional[str],
                                                  node_to_consolidate: Node):

        local_scale_minimizing = Vector3d(0.0000001, 0.0000001, 0.0000001)

        node_to_add = \
            Node(
                name=node_to_consolidate.name,
                position=node_to_consolidate.position,
                local_position=Vector3d(0.0, 0.0, 0.0),
                rotation=node_to_consolidate.rotation,
                local_rotation=QuaternionMathHelper.get_zero_relative_rotation_quaternion(),
                scale=node_to_consolidate.scale,
                local_scale=local_scale_minimizing
            )

        self.nodes_to_add_set.node_in_hierarchy_infos_set.add(
            NodeInHierarchyInfo(node=node_to_add, parent_name=parent_name))

    def build(self) -> BlenderConsolidatedPoseModeAnimationFrameModel:
        return BlenderConsolidatedPoseModeAnimationFrameModel(
            nodes_hierarchy=self.nodes_to_add_set.fullfil_nodes_hierarchy_with_parent_child_chains(
                nodes_hierarchy=self.result_nodes_hierarchy
            ))
