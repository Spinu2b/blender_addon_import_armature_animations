from animations_model.model.armature.blender.blender_edit_mode_armature_model import BlenderEditModeArmatureModel
from animations_model.model.armature.blender.blender_edit_mode_armature_node_model import \
    BlenderEditModeArmatureNodeModel
from animations_model.model.armature.nodes_hierarchy.node import Node
from animations_model.model.armature.nodes_hierarchy.nodes_hierarchy import NodesHierarchy
from animations_model.model.armature.unified_armature_model import UnifiedArmatureModel
from utils.bones_math_helper import BonesMathHelper, AxisInfo, Axis, AxisDirection

from utils.model_spaces_integration.model_vector3d import ModelVector3d


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
        model_axis_info = \
            AxisInfo(
                forward_axis=Axis.Z,
                up_axis=Axis.Y,
                side_axis=Axis.X,
                right_direction_values=AxisDirection.INCREASING_VALUES,
                forward_direction_values=AxisDirection.INCREASING_VALUES,
                up_direction_values=AxisDirection.INCREASING_VALUES
            )

        position = ModelVector3d(
            x=node.position_x, y=node.position_y, z=node.position_z,
            axis_info=model_axis_info
        )
        rotation = ModelVector3d(
            x=node.rotation_x, y=node.rotation_y, z=node.rotation_z,
            axis_info=model_axis_info
        )
        scale = ModelVector3d(
            x=node.scale_x, y=node.scale_y, z=node.scale_z,
            axis_info=model_axis_info
        )

        head_position, tail_position = BonesMathHelper().calculate_head_and_tail_position(
            position=position,
            rotation=rotation,
            scale=scale
        )
        return BlenderEditModeArmatureNodeModel(
            head_position_x=head_position[0],
            head_position_y=head_position[1],
            head_position_z=head_position[2],
            tail_position_x=tail_position[0],
            tail_position_y=tail_position[1],
            tail_position_z=tail_position[2]
        )