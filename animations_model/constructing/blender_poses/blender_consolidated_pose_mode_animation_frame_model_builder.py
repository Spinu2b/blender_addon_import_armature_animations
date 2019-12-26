from typing import Optional

from ....animations_model.constructing.deriving_unified_armature.consolidation.node_in_hierarchy_info import \
    NodeInHierarchyInfo
from ....animations_model.constructing.deriving_unified_armature.consolidation.node_in_hierarchy_infos_set import \
    NodeInHierarchyInfosSet
from ....utils.model_spaces_integration.math_utils import MathUtils
from ....animations_model.model.armature.nodes_hierarchy.node import Node
from ....animations_model.model.armature.nodes_hierarchy.nodes_hierarchy import NodesHierarchy
from ....animations_model.model.blender_poses.blender_consolidated_pose_mode_animation_frame_model import \
    BlenderConsolidatedPoseModeAnimationFrameModel


class BlenderConsolidatedPoseModeAnimationFrameModelBuilder:
    def __init__(self):
        self.result_nodes_hierarchy = NodesHierarchy()
        self.nodes_to_add_set = NodeInHierarchyInfosSet(set())

    def _get_scale(self, scale: float, reference_scale: float) -> float:
        return scale / reference_scale if not MathUtils.is_close_enough_to_zero(reference_scale) else 0.0

    def consolidate_and_add_node(self,
                                 parent_name: Optional[str],
                                 reference: Node,
                                 node_to_consolidate: Node):
        node_to_add = \
            Node(
                name=reference.name,
                position_x=node_to_consolidate.position_x,
                position_y=node_to_consolidate.position_y,
                position_z=node_to_consolidate.position_z,
                local_position_x=node_to_consolidate.position_x - reference.position_x,
                local_position_y=node_to_consolidate.position_y - reference.position_y,
                local_position_z=node_to_consolidate.position_z - reference.position_z,
                rotation_x=node_to_consolidate.rotation_x,
                rotation_y=node_to_consolidate.rotation_y,
                rotation_z=node_to_consolidate.rotation_z,
                local_rotation_x=node_to_consolidate.rotation_x - reference.rotation_x,
                local_rotation_y=node_to_consolidate.rotation_y - reference.rotation_y,
                local_rotation_z=node_to_consolidate.rotation_z - reference.rotation_z,
                scale_x=node_to_consolidate.scale_x,
                scale_y=node_to_consolidate.scale_y,
                scale_z=node_to_consolidate.scale_z,
                local_scale_x=self._get_scale(node_to_consolidate.scale_x, reference.scale_x),
                local_scale_y=self._get_scale(node_to_consolidate.scale_y, reference.scale_y),
                local_scale_z=self._get_scale(node_to_consolidate.scale_z, reference.scale_z),
            )

        self.nodes_to_add_set.node_in_hierarchy_infos_set.add(
            NodeInHierarchyInfo(node=node_to_add, parent_name=parent_name))

    def build(self) -> BlenderConsolidatedPoseModeAnimationFrameModel:
        return BlenderConsolidatedPoseModeAnimationFrameModel(
            nodes_hierarchy=self.nodes_to_add_set.fullfil_nodes_hierarchy_with_parent_child_chains(
                nodes_hierarchy=self.result_nodes_hierarchy
            ))
