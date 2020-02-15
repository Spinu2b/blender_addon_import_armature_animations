from model.animations.json_parsing.animations_parsing.animation_frame_node_model_json_deserializer import \
    AnimationFrameNodeModelJsonDeserializer
from model.animations.model.animations.animation_frame_model import AnimationFrameModel
from utils.json_parsing.string_json_deserializer import StringJsonDeserializer
from utils.json_parsing.tree_json_deserializer import TreeJsonDeserializer


class AnimationFrameModelJsonDeserializer(TreeJsonDeserializer[AnimationFrameModel,
                                                               StringJsonDeserializer,
                                                               AnimationFrameNodeModelJsonDeserializer]):
    pass
