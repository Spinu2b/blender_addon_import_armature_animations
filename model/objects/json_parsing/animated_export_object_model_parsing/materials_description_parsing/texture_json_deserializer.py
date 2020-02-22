from ......model.objects.model.animated_export_object_model_description.materials_description.texture import Texture, Color
from ......utils.json_parsing.float_json_deserializer import FloatJsonDeserializer
from ......utils.json_parsing.int_json_deserializer import IntJsonDeserializer
from ......utils.json_parsing.json_deserializer import JsonDeserializer
from ......utils.json_parsing.list_json_deserializer import ListJsonDeserializer
from ......utils.json_parsing.string_json_deserializer import StringJsonDeserializer


class ColorJsonDeserializer(JsonDeserializer):
    ATTRIBUTES = {
        "red": ("red", FloatJsonDeserializer),
        "green": ("green", FloatJsonDeserializer),
        "blue": ("blue", FloatJsonDeserializer),
        "alpha": ("alpha", FloatJsonDeserializer)
    }
    RESULT_CLASS = Color


class PixelsJsonDeserializer(ListJsonDeserializer):
    LIST_ELEMENT_JSON_DESERIALIZER_CLASS = ColorJsonDeserializer


class TextureJsonDeserializer(JsonDeserializer):
    ATTRIBUTES = {
        "name": ("name", StringJsonDeserializer),
        "width": ("width", IntJsonDeserializer),
        "height": ("height", IntJsonDeserializer),
        "pixels": ("pixels", PixelsJsonDeserializer)
    }
    RESULT_CLASS = Texture
