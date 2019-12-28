from ...utils.model_spaces_integration.quaternion import Quaternion
from ...utils.model_spaces_integration.vector3d import Vector3d
from ...animations_model.model.animations.animation_frame_model import AnimationFrameModel
from ...animations_model.model.animations.animation_frame_node_model import AnimationFrameNodeModel


class AnimationFrameModelBuilder:
    def __init__(self):
        self.animation_frame_model = AnimationFrameModel()

    def _traverse_animation_frame_tree_and_add_node(self, animation_frame_model_node, parent_node_name, root_node):
        if parent_node_name is None:
            self.animation_frame_model.nodes.append(animation_frame_model_node)
            return True
        else:
            add_result_flag = False
            if root_node is None:
                for frame_model_node in self.animation_frame_model.nodes:
                    if frame_model_node.node_name == parent_node_name:
                        frame_model_node.nodes.append(animation_frame_model_node)
                        return True
                    else:
                        add_result_flag = self._traverse_animation_frame_tree_and_add_node(
                            animation_frame_model_node,
                            parent_node_name,
                            frame_model_node)
                if not add_result_flag:
                    raise ValueError("Parent bone not found!")
            else:
                for frame_model_node in root_node.nodes:
                    if frame_model_node.node_name == parent_node_name:
                        frame_model_node.nodes.append(animation_frame_model_node)
                        return True
                    else:
                        add_result_flag = self._traverse_animation_frame_tree_and_add_node(
                            animation_frame_model_node,
                            parent_node_name,
                            frame_model_node)
                return add_result_flag

    def add_skeleton_node_under(self, parent_node_name, node_name,
                                position: Vector3d,
                                local_position: Vector3d,
                                rotation: Quaternion,
                                local_rotation: Quaternion,
                                scale: Vector3d,
                                local_scale: Vector3d):

        animation_frame_model_node = AnimationFrameNodeModel(
            node_name=node_name,
            position=position,
            local_position=local_position,
            rotation=rotation,
            local_rotation=local_rotation,
            scale=scale,
            local_scale=local_scale
        )

        self._traverse_animation_frame_tree_and_add_node(animation_frame_model_node, parent_node_name, root_node=None)

    def build(self):
        return self.animation_frame_model
