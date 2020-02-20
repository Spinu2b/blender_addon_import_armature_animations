from ....model.animations.model.armature_with_animation_clips_model import ArmatureWithAnimationClipsModel
from ....model.animations.json_parsing.animations_parsing.animation_clip_model_json_deserializer import \
    AnimationClipModelJsonDeserializer
from ....utils.json_parsing.dict_json_deserializer import DictJsonDeserializer
from ....utils.json_parsing.json_deserializer import JsonDeserializer
from ....utils.json_parsing.string_json_deserializer import StringJsonDeserializer


class AnimationClipsJsonDeserializer(DictJsonDeserializer):
    KEY_JSON_DESERIALIZER_CLASS = StringJsonDeserializer
    VALUE_JSON_DESERIALIZER_CLASS = AnimationClipModelJsonDeserializer


class ArmatureWithAnimationClipsModelJsonDeserializer(JsonDeserializer):
    ATTRIBUTES = {
        "animationClips": ("animation_clips", AnimationClipsJsonDeserializer)
    }
    RESULT_CLASS = ArmatureWithAnimationClipsModel
