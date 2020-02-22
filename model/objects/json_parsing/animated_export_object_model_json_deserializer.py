from ....model.objects.json_parsing.animated_export_object_model_parsing.materials_description_parsing.\
    material_json_deserializer import MaterialJsonDeserializer
from ....utils.json_parsing.list_json_deserializer import ListJsonDeserializer
from ....model.objects.json_parsing.animated_export_object_model_parsing.bone_bind_pose_json_deserializer import \
    BoneBindPoseJsonDeserializer
from ....utils.json_parsing.dict_json_deserializer import DictJsonDeserializer
from ....model.objects.json_parsing.animated_export_object_model_parsing.mesh_geometry_json_deserializer import \
    MeshGeometryJsonDeserializer
from ....model.objects.model.animated_export_object_model import AnimatedExportObjectModel
from ....model.objects.json_parsing.animated_export_object_model_parsing.transform_model_json_deserializer import \
    TransformModelJsonDeserializer
from ....utils.json_parsing.json_deserializer import JsonDeserializer
from ....utils.json_parsing.string_json_deserializer import StringJsonDeserializer


class BindBonePosesJsonDeserializer(DictJsonDeserializer):
    KEY_JSON_DESERIALIZER_CLASS = StringJsonDeserializer
    VALUE_JSON_DESERIALIZER_CLASS = BoneBindPoseJsonDeserializer


class MaterialsJsonDeserializer(ListJsonDeserializer):
    LIST_ELEMENT_JSON_DESERIALIZER_CLASS = MaterialJsonDeserializer


class AnimatedExportObjectModelJsonDeserializer(JsonDeserializer):
    ATTRIBUTES = {
        "Name": ("name", StringJsonDeserializer),
        "transform": ("transform", TransformModelJsonDeserializer),
        "meshGeometry": ("mesh_geometry", MeshGeometryJsonDeserializer),
        "bindBonePoses": ("bind_bone_poses", BindBonePosesJsonDeserializer),
        "materials": ("materials", MaterialsJsonDeserializer)
    }
    RESULT_CLASS = AnimatedExportObjectModel
