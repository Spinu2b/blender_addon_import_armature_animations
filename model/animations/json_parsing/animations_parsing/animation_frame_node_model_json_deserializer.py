from .....model.animations.model.animations.animation_frame_model import AnimationFrameNodeModel
from .....utils.json_parsing.json_deserializer import JsonDeserializer
from .....utils.json_parsing.quaternion_json_deserializer import QuaternionJsonDeserializer
from .....utils.json_parsing.string_json_deserializer import StringJsonDeserializer
from .....utils.json_parsing.vector3d_json_deserializer import Vector3dJsonDeserializer


class AnimationFrameNodeModelJsonDeserializer(JsonDeserializer):
    ATTRIBUTES = {
        "nodeName": ("node_name", StringJsonDeserializer),
        "position": ("position", Vector3dJsonDeserializer),
        "localPosition": ("local_position", Vector3dJsonDeserializer),
        "rotation": ("rotation", QuaternionJsonDeserializer),
        "localRotation": ("local_rotation", QuaternionJsonDeserializer),
        "scale": ("scale", Vector3dJsonDeserializer),
        "localScale": ("local_scale", Vector3dJsonDeserializer)
    }
    RESULT_CLASS = AnimationFrameNodeModel
