from typing import Dict

from animations_model.constructing.deriving_unified_armature.\
    unified_armature_model_constructor import UnifiedArmatureModelConstructor
from animations_model.model.animations.animation_clip_model import AnimationClipModel
from animations_model.model.armature.unified_armature_model import UnifiedArmatureModel


class ArmatureWithAnimationClipsModel:
    def __init__(self):
        self.animation_clips = dict()  # type: Dict[str, AnimationClipModel]

    def get_unified_armature_model(self) -> UnifiedArmatureModel:
        unified_armature_model_constructor = UnifiedArmatureModelConstructor()
        unified_armature_model = unified_armature_model_constructor.\
            derive_unified_armature_model_from_animation_clips(self.animation_clips)
        return unified_armature_model

    def get_animation_clips(self) -> Dict[str, AnimationClipModel]:
        return self.animation_clips
