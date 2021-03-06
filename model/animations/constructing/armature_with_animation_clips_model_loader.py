import json
from typing import TYPE_CHECKING

from ....model.animations.constructing.armature_with_animation_clips_model_constructor import\
    ArmatureWithAnimationClipsModelConstructor

if TYPE_CHECKING:
    from ....model.animations.model.armature_with_animation_clips_model import ArmatureWithAnimationClipsModel


class ArmatureWithAnimationClipsModelLoader:
    def load(cls, path_to_json_file: str) -> 'ArmatureWithAnimationClipsModel':
        with open(path_to_json_file, 'r') as json_file:
            json_dict = json.loads(json_file.read())
        return ArmatureWithAnimationClipsModelConstructor().construct_from_json(json_dict)
