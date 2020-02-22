from .....model.animations.model.animations.animation_clip_model import AnimationClipModel
from .....model.animations.model.animations.animation_frame_model import AnimationFrameModel
from .....model.animations.json_parsing.animations_parsing.animation_frame_model_json_deserializer import \
    AnimationFrameModelJsonDeserializer
from .....utils.json_parsing.dict_json_deserializer import DictJsonDeserializer, DictJsonBuildingListener
from .....utils.json_parsing.int_json_deserializer import IntJsonDeserializer


class AnimationClipModelBuildingResultListener(DictJsonBuildingListener):
    RESULT = None

    @classmethod
    def on_init(cls):
        cls.RESULT = AnimationClipModel()

    @classmethod
    def on_key_value_parsing(cls, key: int, value: AnimationFrameModel):
        cls.RESULT.frames[key] = value

    @classmethod
    def get_result(cls) -> AnimationClipModel:
        result = cls.RESULT
        cls.RESULT = None
        return result


class AnimationClipModelJsonDeserializer(DictJsonDeserializer):
    KEY_JSON_DESERIALIZER_CLASS = IntJsonDeserializer
    VALUE_JSON_DESERIALIZER_CLASS = AnimationFrameModelJsonDeserializer
    DICT_BUILDING_RESULT_LISTENER = AnimationClipModelBuildingResultListener
