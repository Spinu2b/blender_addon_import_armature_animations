from typing import Tuple

from .....utils.json_parsing.json_parsing_helper import JsonParsingHelper
from .....model.objects.model.animated_export_object_model_description.mesh_geometry import MeshGeometry
from .....utils.json_parsing.dict_json_deserializer import DictJsonDeserializer
from .....utils.json_parsing.float_json_deserializer import FloatJsonDeserializer
from .....utils.json_parsing.int_json_deserializer import IntJsonDeserializer
from .....utils.json_parsing.json_deserializer import JsonDeserializer
from .....utils.json_parsing.list_json_deserializer import ListJsonDeserializer
from .....utils.json_parsing.string_json_deserializer import StringJsonDeserializer
from .....utils.json_parsing.vector2d_json_deserializer import Vector2dJsonDeserializer
from .....utils.json_parsing.vector3d_json_deserializer import Vector3dJsonDeserializer


class CSharpTriangleTupleJsonDeserializer(JsonDeserializer):
    @classmethod
    def deserialize(cls, json_string: str, parsing_start_char_index: int = 0) -> Tuple[Tuple[int, int, int], int]:
        attribute_name, parsing_start_char_index = JsonParsingHelper.get_next_attribute_in_json_object(
            json_string, parsing_start_char_index)
        item1_value, parsing_start_char_index = \
            IntJsonDeserializer.deserialize(json_string=json_string,
                                            parsing_start_char_index=parsing_start_char_index)
        attribute_name, parsing_start_char_index = JsonParsingHelper.get_next_attribute_in_json_object(
            json_string, parsing_start_char_index)
        item2_value, parsing_start_char_index = \
            IntJsonDeserializer.deserialize(json_string=json_string,
                                            parsing_start_char_index=parsing_start_char_index)
        attribute_name, parsing_start_char_index = JsonParsingHelper.get_next_attribute_in_json_object(
            json_string, parsing_start_char_index)
        item3_value, parsing_start_char_index = \
            IntJsonDeserializer.deserialize(json_string=json_string,
                                            parsing_start_char_index=parsing_start_char_index)

        parsing_start_char_index = JsonParsingHelper.go_to_the_end_of_that_json_object(
            json_string=json_string, parsing_start_char_index=parsing_start_char_index)

        return (item1_value, item2_value, item3_value), parsing_start_char_index


class VerticesJsonDeserializer(ListJsonDeserializer):
    LIST_ELEMENT_JSON_DESERIALIZER_CLASS = Vector3dJsonDeserializer


class TrianglesJsonDeserializer(ListJsonDeserializer):
    LIST_ELEMENT_JSON_DESERIALIZER_CLASS = CSharpTriangleTupleJsonDeserializer


class NormalsJsonDeserializer(ListJsonDeserializer):
    LIST_ELEMENT_JSON_DESERIALIZER_CLASS = Vector3dJsonDeserializer


class BonesWeightsJsonDeserializer(DictJsonDeserializer):
    class VerticesWeightsJsonDeserializer(DictJsonDeserializer):
        KEY_JSON_DESERIALIZER_CLASS = IntJsonDeserializer
        VALUE_JSON_DESERIALIZER_CLASS = FloatJsonDeserializer

    KEY_JSON_DESERIALIZER_CLASS = StringJsonDeserializer
    VALUE_JSON_DESERIALIZER_CLASS = VerticesWeightsJsonDeserializer


class UvMapsJsonDeserializer(ListJsonDeserializer):
    LIST_ELEMENT_JSON_DESERIALIZER_CLASS = Vector2dJsonDeserializer


class MeshGeometryJsonDeserializer(JsonDeserializer):
    ATTRIBUTES = {
        "vertices": ("vertices", VerticesJsonDeserializer),
        "triangles": ("triangles", TrianglesJsonDeserializer),
        "normals": ("normals", NormalsJsonDeserializer),
        "bonesWeights": ("bones_weights", BonesWeightsJsonDeserializer),
        "uvMaps": ("uv_maps", UvMapsJsonDeserializer)
    }
    RESULT_CLASS = MeshGeometry
