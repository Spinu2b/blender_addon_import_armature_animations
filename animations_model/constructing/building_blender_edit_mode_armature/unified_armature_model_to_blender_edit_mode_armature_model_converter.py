from animations_model.model.armature.blender.blender_edit_mode_armature_model import BlenderEditModeArmatureModel
from animations_model.model.armature.blender.blender_edit_mode_armature_node_model import \
    BlenderEditModeArmatureNodeModel
from animations_model.model.armature.nodes_hierarchy.node import Node
from animations_model.model.armature.nodes_hierarchy.nodes_hierarchy import NodesHierarchy
from animations_model.model.armature.unified_armature_model import UnifiedArmatureModel
from utils.bones_math_helper import BonesMathHelper


class UnifiedArmatureModelToBlenderEditModeArmatureModelConverter:
    def convert(self, unified_armature_model: UnifiedArmatureModel) -> BlenderEditModeArmatureModel:
        nodes_hierarchy = unified_armature_model.nodes_hierarchy  # type: NodesHierarchy
        result = BlenderEditModeArmatureModel()
        for node_iter in nodes_hierarchy.iterate_nodes():
            result.add_node(
                parent_name=node_iter.parent.name if node_iter.parent is not None else None,
                node=self._get_blender_edit_mode_armature_node(node_iter.node))
        return result

    def _get_blender_edit_mode_armature_node(self, node: Node) -> BlenderEditModeArmatureNodeModel:
        head_position, tail_position = BonesMathHelper.calculate_head_and_tail_position(
            position=(node.position_x, node.position_y, node.position_z),
            rotation=(node.rotation_x, node.rotation_y, node.rotation_z),
            scale=(node.scale_x, node.scale_y, node.scale_z)
        )
        return BlenderEditModeArmatureNodeModel(
            head_position_x=head_position[0],
            head_position_y=head_position[1],
            head_position_z=head_position[2],
            tail_position_x=tail_position[0],
            tail_position_y=tail_position[1],
            tail_position_z=tail_position[2]
        )
