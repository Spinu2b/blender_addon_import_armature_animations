from ...utils.model_spaces_integration.quaternion import Quaternion
from ...utils.model_spaces_integration.vector3d import Vector3d
from ...animations_model.constructing.animation_frame_model_builder import AnimationFrameModelBuilder
from ...animations_model.model.animations.animation_clip_model import AnimationClipModel
from ...animations_model.model.armature_with_animation_clips_model import ArmatureWithAnimationClipsModel


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
                position=Vector3d(
                    x=skeleton_subpart_node["positionX"],
                    y=skeleton_subpart_node["positionY"],
                    z=skeleton_subpart_node["positionZ"]
                ),
                local_position=Vector3d(
                    x=skeleton_subpart_node["localPositionX"],
                    y=skeleton_subpart_node["localPositionY"],
                    z=skeleton_subpart_node["localPositionZ"]
                ),
                rotation=Quaternion(
                    w=skeleton_subpart_node["rotationW"],
                    x=skeleton_subpart_node["rotationX"],
                    y=skeleton_subpart_node["rotationY"],
                    z=skeleton_subpart_node["rotationZ"]
                ),
                local_rotation=Quaternion(
                    w=skeleton_subpart_node["localRotationW"],
                    x=skeleton_subpart_node["localRotationX"],
                    y=skeleton_subpart_node["localRotationY"],
                    z=skeleton_subpart_node["localRotationZ"]
                ),
                scale=Vector3d(
                    x=skeleton_subpart_node["scaleX"],
                    y=skeleton_subpart_node["scaleY"],
                    z=skeleton_subpart_node["scaleZ"]
                ),
                local_scale=Vector3d(
                    x=skeleton_subpart_node["localScaleX"],
                    y=skeleton_subpart_node["localScaleY"],
                    z=skeleton_subpart_node["localScaleZ"]
                )
            )

            self._traverse_bones_tree_and_build_animation_frame_model(
                root_nodes=skeleton_subpart_node["children"],
                animation_frame_model_builder=animation_frame_model_builder,
                root_node_name=skeleton_subpart_node["boneName"]
            )

    def build(self):
        return self.armature_with_animation_clips_model
