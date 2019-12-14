from animations_model.model.animations.animation_frame_model import AnimationFrameModel
from animations_model.model.animations.animation_frame_node_model import AnimationFrameNodeModel


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
                                position_x, position_y, position_z,
                                local_position_x, local_position_y, local_position_z,
                                rotation_x, rotation_y, rotation_z,
                                local_rotation_x, local_rotation_y, local_rotation_z,
                                scale_x, scale_y, scale_z,
                                local_scale_x, local_scale_y, local_scale_z):

        animation_frame_model_node = AnimationFrameNodeModel(
            node_name=node_name,
            position_x=position_x,
            position_y=position_y,
            position_z=position_z,
            local_position_x=local_position_x,
            local_position_y=local_position_y,
            local_position_z=local_position_z,
            rotation_x=rotation_x,
            rotation_y=rotation_y,
            rotation_z=rotation_z,
            local_rotation_x=local_rotation_x,
            local_rotation_y=local_rotation_y,
            local_rotation_z=local_rotation_z,
            scale_x=scale_x,
            scale_y=scale_y,
            scale_z=scale_z,
            local_scale_x=local_scale_x,
            local_scale_y=local_scale_y,
            local_scale_z=local_scale_z
        )

        self._traverse_animation_frame_tree_and_add_node(animation_frame_model_node, parent_node_name, root_node=None)

    def build(self):
        return self.animation_frame_model
