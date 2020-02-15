from utils.json_parsing.float_json_deserializer import FloatJsonDeserializer
from utils.json_parsing.json_deserializer import JsonDeserializer
from utils.model_spaces_integration.vector2d import Vector2d


class Vector2dJsonDeserializer(JsonDeserializer):
    ATTRIBUTES = {
        "x": ("x", FloatJsonDeserializer),
        "y": ("y", FloatJsonDeserializer)
    }
    RESULT_CLASS = Vector2d
