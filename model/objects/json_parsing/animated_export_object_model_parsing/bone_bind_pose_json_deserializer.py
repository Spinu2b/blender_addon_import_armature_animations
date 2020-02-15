from .....model.objects.model.animated_export_object_model_description.bone_bind_pose import BoneBindPose
from .....utils.json_parsing.json_deserializer import JsonDeserializer
from .....utils.json_parsing.quaternion_json_deserializer import QuaternionJsonDeserializer
from .....utils.json_parsing.vector3d_json_deserializer import Vector3dJsonDeserializer


class BoneBindPoseJsonDeserializer(JsonDeserializer):
    ATTRIBUTES = {
        "position": ("position", Vector3dJsonDeserializer),
        "rotation": ("rotation", QuaternionJsonDeserializer),
        "scale": ("scale", Vector3dJsonDeserializer)
    }
    RESULT_CLASS = BoneBindPose
