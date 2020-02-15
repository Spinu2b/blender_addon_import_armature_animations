from utils.json_parsing.float_json_deserializer import FloatJsonDeserializer
from utils.json_parsing.json_deserializer import JsonDeserializer
from utils.model_spaces_integration.quaternion import Quaternion


class QuaternionJsonDeserializer(JsonDeserializer):
    ATTRIBUTES = {
        "w": ("w", FloatJsonDeserializer),
        "x": ("x", FloatJsonDeserializer),
        "y": ("y", FloatJsonDeserializer),
        "z": ("z", FloatJsonDeserializer)
    }
    RESULT_CLASS = Quaternion
