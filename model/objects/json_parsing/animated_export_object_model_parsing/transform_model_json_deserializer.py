from .....model.objects.model.animated_export_object_model_description.transform_model import TransformModel
from .....utils.json_parsing.json_deserializer import JsonDeserializer
from .....utils.json_parsing.quaternion_json_deserializer import QuaternionJsonDeserializer
from .....utils.json_parsing.vector3d_json_deserializer import Vector3dJsonDeserializer


class TransformModelJsonDeserializer(JsonDeserializer):
    ATTRIBUTES = {
        "position": ("position", Vector3dJsonDeserializer),
        "rotation": ("rotation", QuaternionJsonDeserializer),
        "scale": ("scale", Vector3dJsonDeserializer),
        "localPosition": ("local_position", Vector3dJsonDeserializer),
        "localRotation": ("local_rotation", QuaternionJsonDeserializer),
        "localScale": ("local_scale", Vector3dJsonDeserializer),
    }
    RESULT_CLASS = TransformModel
