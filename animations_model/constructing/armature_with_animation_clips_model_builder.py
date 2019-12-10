from animations_model.constructing.animation_frame_model_builder import AnimationFrameModelBuilder
from animations_model.model.animation_clip_model import AnimationClipModel
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
                rotation_x=skeleton_subpart_node["rotationX"],
                rotation_y=skeleton_subpart_node["rotationY"],
                rotation_z=skeleton_subpart_node["rotationZ"],
                scale_x=skeleton_subpart_node["scaleX"],
                scale_y=skeleton_subpart_node["scaleY"],
                scale_z=skeleton_subpart_node["scaleZ"]
            )

            self._traverse_bones_tree_and_build_animation_frame_model(
                root_nodes=skeleton_subpart_node["children"],
                animation_frame_model_builder=animation_frame_model_builder,
                root_node_name=skeleton_subpart_node["boneName"]
            )

    def build(self):
        return self.armature_with_animation_clips_model
