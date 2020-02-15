from model.objects.json_parsing.animated_export_object_model_parsing.transform_model_json_deserializer import \
    TransformModelJsonDeserializer
from utils.json_parsing.json_deserializer import JsonDeserializer
from utils.json_parsing.string_json_deserializer import StringJsonDeserializer


class AnimatedExportObjectModelJsonDeserializer(JsonDeserializer):
    ATTRIBUTES = {
        "Name": ("name", StringJsonDeserializer),
        "transform": ("transform", TransformModelJsonDeserializer),
    }
