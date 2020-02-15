from model.objects.json_parsing.animated_export_object_model_parsing.materials_description_parsing.\
    texture_json_deserializer import \
    TextureJsonDeserializer
from model.objects.model.animated_export_object_model_description.materials_description.material import Material
from utils.json_parsing.json_deserializer import JsonDeserializer
from utils.json_parsing.string_json_deserializer import StringJsonDeserializer
from utils.json_parsing.vector2d_json_deserializer import Vector2dJsonDeserializer


class MaterialJsonDeserializer(JsonDeserializer):
    ATTRIBUTES = {
        "mainTexture": ("main_texture", TextureJsonDeserializer),
        "mainTextureOffset": ("main_texture_offset", Vector2dJsonDeserializer),
        "mainTextureScale": ("main_texture_scale", Vector2dJsonDeserializer),
        "name": ("name", StringJsonDeserializer)
    }
    RESULT_CLASS = Material
