from utils.json_parsing.float_json_deserializer import FloatJsonDeserializer
from utils.json_parsing.json_deserializer import JsonDeserializer
from utils.model_spaces_integration.vector3d import Vector3d


class Vector3dJsonDeserializer(JsonDeserializer):
    ATTRIBUTES = {
        "x": ("x", FloatJsonDeserializer),
        "y": ("y", FloatJsonDeserializer),
        "z": ("z", FloatJsonDeserializer)
    }
    RESULT_CLASS = Vector3d
