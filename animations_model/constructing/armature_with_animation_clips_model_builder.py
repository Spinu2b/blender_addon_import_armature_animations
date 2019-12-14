from animations_model.constructing.animation_frame_model_builder import AnimationFrameModelBuilder
from animations_model.model.animations.animation_clip_model import AnimationClipModel
from animations_model.model.armature_with_animation_clips_model import ArmatureWithAnimationClipsModel


class ArmatureWithAnimationClipsModelBuilder:
    def __init__(self):
        self.armature_with_animation_clips_model = ArmatureWithAnimationClipsModel()

    def add_animation_clip(self, animation_clip_name):
        self.armature_with_animation_clips_model.animation_clips[animation_clip_name] =\
            AnimationClipModel(animation_clip_name)

    def add_frame_to_animation_clip(self, animation_clip_name, animation_frame_dict, animation_frame_number):
        animation_frame_model_builder = AnimationFrameModelBuilder()
        self._traverse_bones_tree_and_build_animation_frame_model(
            root_nodes=animation_frame_dict['nodes'],
            animation_frame_model_builder=animation_frame_model_builder,
            root_node_name=None)
        animation_frame_model = animation_frame_model_builder.build()
        self.armature_with_animation_clips_model.animation_clips[animation_clip_name]. \
            frames[animation_frame_number] = animation_frame_model

    def _traverse_bones_tree_and_build_animation_frame_model(self, root_nodes, animation_frame_model_builder,
                                                             root_node_name=None):
        for skeleton_subpart_node in root_nodes:
            animation_frame_model_builder.add_skeleton_node_under(
                parent_node_name=root_node_name,
                node_name=skeleton_subpart_node["boneName"],
                position_x=skeleton_subpart_node["positionX"],
                position_y=skeleton_subpart_node["positionY"],
                position_z=skeleton_subpart_node["positionZ"],
                local_position_x=skeleton_subpart_node["localPositionX"],
                local_position_y=skeleton_subpart_node["localPositionY"],
                local_position_z=skeleton_subpart_node["localPositionZ"],
                rotation_x=skeleton_subpart_node["rotationX"],
                rotation_y=skeleton_subpart_node["rotationY"],
                rotation_z=skeleton_subpart_node["rotationZ"],
                local_rotation_x=skeleton_subpart_node["localRotationX"],
                local_rotation_y=skeleton_subpart_node["localRotationY"],
                local_rotation_z=skeleton_subpart_node["localRotationZ"],
                scale_x=skeleton_subpart_node["scaleX"],
                scale_y=skeleton_subpart_node["scaleY"],
                scale_z=skeleton_subpart_node["scaleZ"],
                local_scale_x=skeleton_subpart_node["localScaleX"],
                local_scale_y=skeleton_subpart_node["localScaleY"],
                local_scale_z=skeleton_subpart_node["localScaleZ"]
            )

            self._traverse_bones_tree_and_build_animation_frame_model(
                root_nodes=skeleton_subpart_node["children"],
                animation_frame_model_builder=animation_frame_model_builder,
                root_node_name=skeleton_subpart_node["boneName"]
            )

    def build(self):
        return self.armature_with_animation_clips_model
