from ....model.animations.model.animations.animation_frame_model import AnimationFrameModel, AnimationFrameNodeModel
from ....utils.model.json_dict_tree_builder import JsonDictTreeBuilder
from ....model.animations.model.animations.animation_clip_model import AnimationClipModel
from ....model.animations.model.armature_with_animation_clips_model import ArmatureWithAnimationClipsModel


class ArmatureWithAnimationClipsModelBuilder:
    def __init__(self):
        self.armature_with_animation_clips_model = ArmatureWithAnimationClipsModel()

    def add_animation_clip(self, animation_clip_name):
        self.armature_with_animation_clips_model.animation_clips[animation_clip_name] =\
            AnimationClipModel(animation_clip_name)
        return self

    def add_frame_to_animation_clip(self, animation_clip_name, animation_frame_dict, animation_frame_number):
        animation_frame_model = JsonDictTreeBuilder().build_from(
            AnimationFrameModel, AnimationFrameNodeModel, animation_frame_dict)
        self.armature_with_animation_clips_model.animation_clips[animation_clip_name]. \
            frames[animation_frame_number] = animation_frame_model
        return self

    def build(self):
        return self.armature_with_animation_clips_model
