import copy
from typing import Dict
from typing import TYPE_CHECKING

from ...animations_model.constructing.deriving_unified_armature.\
    unified_armature_model_constructor import UnifiedArmatureModelConstructor

if TYPE_CHECKING:
    from ...animations_model.model.animations.animation_clip_model import AnimationClipModel
    from ...animations_model.model.armature.unified_armature_model import UnifiedArmatureModel


class ArmatureWithAnimationClipsModel:
    def __init__(self):
        self.animation_clips = dict()  # type: Dict[str, AnimationClipModel]

    def get_unified_armature_model(self) -> 'UnifiedArmatureModel':
        unified_armature_model_constructor = UnifiedArmatureModelConstructor()
        unified_armature_model = unified_armature_model_constructor.\
            derive_unified_armature_model_from_animation_clips(self.animation_clips)
        return unified_armature_model

    def get_animation_clips(self) -> Dict[str, 'AnimationClipModel']:
        return self.animation_clips

    def remove_animation_clips_longer_than(self, frames_count: int):
        self.animation_clips = {animation_clip_name: self.animation_clips[animation_clip_name]
                                for animation_clip_name in self.animation_clips if
                                len(self.animation_clips[animation_clip_name].frames) <= frames_count}
