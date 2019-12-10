from animations_model.constructing.deriving_unified_armature.unified_armature_model_constructor import UnifiedArmatureModelConstructor


class ArmatureWithAnimationClipsModel:
    def __init__(self):
        self.animation_clips = dict()

    def get_unified_armature_model(self):
        unified_armature_model_constructor = UnifiedArmatureModelConstructor()
        unified_armature_model = unified_armature_model_constructor.\
            derive_unified_armature_model_from_animation_clips(self.animation_clips)
        return unified_armature_model
