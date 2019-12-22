from typing import Optional

from animations_model.model.armature.nodes_hierarchy.node import Node
from animations_model.model.armature.nodes_hierarchy.nodes_hierarchy import NodesHierarchy
from animations_model.model.blender_poses.blender_consolidated_pose_mode_animation_frame_model import \
    BlenderConsolidatedPoseModeAnimationFrameModel


class BlenderConsolidatedPoseModeAnimationFrameModelBuilder:
    def __init__(self):
        self.result_nodes_hierarchy = NodesHierarchy()

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
                local_scale_x=node_to_consolidate.scale_x / reference.scale_x,
                local_scale_y=node_to_consolidate.scale_y / reference.scale_y,
                local_scale_z=node_to_consolidate.scale_z / reference.scale_z
            )

        self.result_nodes_hierarchy.add_node(parent_name=parent_name, node=node_to_add)

    def build(self) -> BlenderConsolidatedPoseModeAnimationFrameModel:
        return BlenderConsolidatedPoseModeAnimationFrameModel(nodes_hierarchy=self.result_nodes_hierarchy)
