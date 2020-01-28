from typing import TYPE_CHECKING

from .....model.animations.model.blender_edit_mode_armature_model import BlenderEditModeArmatureModel, \
    BlenderEditModeArmatureNodeModel
from .....utils.blender.edit_mode_bones.blender_edit_mode_bones_construction_helper import \
    BlenderEditModeBonesConstructionHelper

if TYPE_CHECKING:
    from .....model.objects.model.export_objects_library_model_description.armature_bind_pose_model import \
        ArmatureBindPoseModel, ArmatureBindPoseModelNode


class ArmatureBindPoseModelToBlenderEditModeArmatureModelConverter:
    def convert(self, armature_bind_pose_model: 'ArmatureBindPoseModel') -> BlenderEditModeArmatureModel:
        result = BlenderEditModeArmatureModel()
        for node_iter in armature_bind_pose_model.iterate_nodes():
            result.add_node(
                parent_key=node_iter.parent.name if node_iter.parent is not None else None,
                node_key=node_iter.key,
                node=self._get_blender_edit_mode_armature_node(node_iter.node))
        return result

    def _get_blender_edit_mode_armature_node(
            self, node: 'ArmatureBindPoseModelNode') -> BlenderEditModeArmatureNodeModel:

        head_position, tail_position = BlenderEditModeBonesConstructionHelper().calculate_head_and_tail_position(
            position=node.position,
            rotation=node.rotation,
            scale=node.scale
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
