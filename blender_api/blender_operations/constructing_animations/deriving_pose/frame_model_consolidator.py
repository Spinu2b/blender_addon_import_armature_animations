from typing import TYPE_CHECKING

from .....animations_model.constructing.blender_poses.blender_consolidated_pose_mode_animation_frame_model_builder\
    import BlenderConsolidatedPoseModeAnimationFrameModelBuilder

if TYPE_CHECKING:
    from .....animations_model.model.armature.nodes_hierarchy.nodes_hierarchy import NodesHierarchy
    from .....animations_model.model.blender_poses.blender_consolidated_pose_mode_animation_frame_model import \
        BlenderConsolidatedPoseModeAnimationFrameModel


class FrameModelConsolidator:
    def consolidate(self,
                    unified_armature_model_nodes_hierarchy: 'NodesHierarchy',
                    animation_frame_model_nodes_hierarchy: 'NodesHierarchy') ->\
            'BlenderConsolidatedPoseModeAnimationFrameModel':
        result_builder = BlenderConsolidatedPoseModeAnimationFrameModelBuilder()
        for animation_frame_model_node_iter in animation_frame_model_nodes_hierarchy.iterate_nodes():
            if animation_frame_model_node_iter.node.name not in\
                    unified_armature_model_nodes_hierarchy.get_nodes_names():
                raise ValueError("Animation frame to consolidate contains node that armature doesn't!")

            complementary_armature_node_info = unified_armature_model_nodes_hierarchy.get_node(
                name=animation_frame_model_node_iter.node.name
            )

            result_builder.consolidate_and_add_node(
                parent_name=complementary_armature_node_info.parent_name,
                reference=complementary_armature_node_info.node,
                node_to_consolidate=animation_frame_model_node_iter.node
            )

        self._consolidate_not_used_bones_in_armature(
            result_builder,
            unified_armature_model_nodes_hierarchy,
            animation_frame_model_nodes_hierarchy)

        return result_builder.build()

    def _consolidate_not_used_bones_in_armature(
            self,
            builder: BlenderConsolidatedPoseModeAnimationFrameModelBuilder,
            unified_armature_model_nodes_hierarchy: 'NodesHierarchy',
            animation_frame_model_nodes_hierarchy: 'NodesHierarchy'):
        nodes_names_not_present_in_animation_frame = \
            set(unified_armature_model_nodes_hierarchy.get_nodes_names()) \
            .difference(set(animation_frame_model_nodes_hierarchy.get_nodes_names()))

        for not_present_node_name in nodes_names_not_present_in_animation_frame:
            node_obj_info = unified_armature_model_nodes_hierarchy.get_node(name=not_present_node_name)
            builder.consolidate_non_present_bone_and_add_node(
                parent_name=node_obj_info.parent_name,
                node_to_consolidate=node_obj_info.node
            )
