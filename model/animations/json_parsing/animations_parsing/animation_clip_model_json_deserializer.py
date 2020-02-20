from .....model.animations.model.animations.animation_clip_model import AnimationClipModel
from .....model.animations.json_parsing.animations_parsing.animation_frame_model_json_deserializer import \
    AnimationFrameModelJsonDeserializer
from .....utils.json_parsing.dict_json_deserializer import DictJsonDeserializer
from .....utils.json_parsing.int_json_deserializer import IntJsonDeserializer
from .....utils.json_parsing.json_deserializer import JsonDeserializer
from .....utils.json_parsing.string_json_deserializer import StringJsonDeserializer


class FramesJsonDeserializer(DictJsonDeserializer):
    KEY_JSON_DESERIALIZER_CLASS = IntJsonDeserializer
    VALUE_JSON_DESERIALIZER_CLASS = AnimationFrameModelJsonDeserializer


class AnimationClipModelJsonDeserializer(JsonDeserializer):
    ATTRIBUTES = {
        "animationClipName": ("animation_clip_name", StringJsonDeserializer),
        "frames": ("frames", FramesJsonDeserializer)
    }
    RESULT_CLASS = AnimationClipModel
