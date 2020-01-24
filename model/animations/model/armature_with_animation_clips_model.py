import copy
from typing import Dict

from ....model.objects.model.export_objects_library_model_description.armature_hierarchy_model import\
    ArmatureHierarchyModel
from ....model.animations.model.animations.animation_clip_model import AnimationClipModel


class AnimationClipsFilter:
    @classmethod
    def is_matching_armature_hierarchy(
            cls,
            armature_hierarchy_model: ArmatureHierarchyModel,
            animation_clip: AnimationClipModel) -> bool:
        armature_parent_child_pairs_set = set(armature_hierarchy_model.iterate_parent_child_key_pairs())
        animation_clip_parent_child_pairs_set = \
            set(animation_clip.get_first_animation_frame().iterate_parent_child_key_pairs())
        return animation_clip_parent_child_pairs_set.issubset(armature_parent_child_pairs_set)


class ArmatureWithAnimationClipsModel:
    def __init__(self):
        self.animation_clips = dict()  # type: Dict[str, AnimationClipModel]

    def get_animation_clips(self) -> Dict[str, 'AnimationClipModel']:
        return self.animation_clips

    def remove_animation_clips_longer_than(self, frames_count: int):
        self.animation_clips = {animation_clip_name: self.animation_clips[animation_clip_name]
                                for animation_clip_name in self.animation_clips if
                                len(self.animation_clips[animation_clip_name].frames) <= frames_count}

    def filter_to_only_animation_clips_matching_armature(self, armature_hierarchy_model: ArmatureHierarchyModel):
        result = ArmatureWithAnimationClipsModel()
        result.animation_clips = \
            {animation_clip_name: copy.deepcopy(self.animation_clips[animation_clip_name])
             for animation_clip_name in result.animation_clips
             if AnimationClipsFilter.is_matching_armature_hierarchy(
                armature_hierarchy_model=armature_hierarchy_model,
                animation_clip=self.animation_clips[animation_clip_name])}
        return result
