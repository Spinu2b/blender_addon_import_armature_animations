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
    pass


class MeshGeometryJsonDeserializer(JsonDeserializer):
    ATTRIBUTES = {
        "vertices": ("vertices", ListJsonDeserializer[Vector3dJsonDeserializer]),
        "triangles": ("triangles", ListJsonDeserializer[CSharpTriangleTupleJsonDeserializer]),
        "normals": ("normals", ListJsonDeserializer[Vector3dJsonDeserializer]),
        "bonesWeights": ("bones_weights", DictJsonDeserializer[
            StringJsonDeserializer, DictJsonDeserializer[IntJsonDeserializer, FloatJsonDeserializer]]),
        "uvMaps": ("uv_maps", ListJsonDeserializer[ListJsonDeserializer[Vector2dJsonDeserializer]])
    }
    RESULT_CLASS = MeshGeometry
