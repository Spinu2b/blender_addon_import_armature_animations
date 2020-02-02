from ......model.objects.model.export_objects_library_model_description.materials_description.texture import Texture
from ......utils.model_spaces_integration.vector2d import Vector2d


class Material:
    def __init__(self):
        self.main_texture = Texture()  # type: Texture
        self.main_texture_offset = Vector2d(0.0, 0.0)  # type: Vector2d
        self.main_texture_scale = Vector2d(1.0, 1.0)  # type: Vector2d
        self.name = ""  # type: str
