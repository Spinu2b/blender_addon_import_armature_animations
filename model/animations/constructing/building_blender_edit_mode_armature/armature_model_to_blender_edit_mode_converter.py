from typing import TYPE_CHECKING

from ....utils.model_spaces_integration.model_quaternion import ModelQuaternion
from ....animations_model.model.armature.blender.blender_edit_mode_armature_model import BlenderEditModeArmatureModel
from ....animations_model.model.armature.blender.blender_edit_mode_armature_node_model import \
    BlenderEditModeArmatureNodeModel
from ....utils.blender.edit_mode_bones.blender_edit_mode_bones_construction_helper import \
    BlenderEditModeBonesConstructionHelper
from ....utils.model_spaces_integration.model_vector3d import ModelVector3d

if TYPE_CHECKING:
    from ....animations_model.model.armature.nodes_hierarchy.node import Node
    from ....animations_model.model.armature.nodes_hierarchy.nodes_hierarchy import NodesHierarchy
    from ....animations_model.model.armature.unified_armature_model import UnifiedArmatureModel
    from ....utils.model_spaces_integration.axis_info import AxisInfo


class UnifiedArmatureModelToBlenderEditModeArmatureModelConverter:
    def convert(self, unified_armature_model: 'UnifiedArmatureModel', base_space_model: 'AxisInfo') ->\
                BlenderEditModeArmatureModel:
        nodes_hierarchy = unified_armature_model.nodes_hierarchy  # type: NodesHierarchy
        result = BlenderEditModeArmatureModel()
        for node_iter in nodes_hierarchy.iterate_nodes():
            result.add_node(
                parent_name=node_iter.parent.name if node_iter.parent is not None else None,
                node=self._get_blender_edit_mode_armature_node(node_iter.node, base_space_model))
        return result

    def _get_blender_edit_mode_armature_node(
            self, node: 'Node', base_space_model: 'AxisInfo') -> BlenderEditModeArmatureNodeModel:

        position = ModelVector3d(
            x=node.position.x, y=node.position.y, z=node.position.z,
            axis_info=base_space_model
        )
        rotation = ModelQuaternion(
            w=node.rotation.w, x=node.rotation.x, y=node.rotation.y, z=node.rotation.z,
            axis_info=base_space_model
        )
        scale = ModelVector3d(
            x=node.scale.x, y=node.scale.y, z=node.scale.z,
            axis_info=base_space_model
        )

        head_position, tail_position = BlenderEditModeBonesConstructionHelper().calculate_head_and_tail_position(
            position=position,
            rotation=rotation,
            scale=scale
        )
        return BlenderEditModeArmatureNodeModel(
            name=node.name,
            head_position_x=head_position[0],
            head_position_y=head_position[1],
            head_position_z=head_position[2],
            tail_position_x=tail_position[0],
            tail_position_y=tail_position[1],
            tail_position_z=tail_position[2]
        )
