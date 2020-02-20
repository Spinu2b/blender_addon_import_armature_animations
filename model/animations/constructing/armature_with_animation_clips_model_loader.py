import json
from typing import TYPE_CHECKING

from model.animations.json_parsing.armature_with_animation_clips_model_json_deserializer import \
    ArmatureWithAnimationClipsModelJsonDeserializer
from ....model.animations.constructing.armature_with_animation_clips_model_constructor import\
    ArmatureWithAnimationClipsModelConstructor

if TYPE_CHECKING:
    from ....model.animations.model.armature_with_animation_clips_model import ArmatureWithAnimationClipsModel


class ArmatureWithAnimationClipsModelLoader:
    def load(cls, path_to_json_file: str) -> 'ArmatureWithAnimationClipsModel':
        with open(path_to_json_file, 'r') as json_file:
            json_string = json_file.read()
        return ArmatureWithAnimationClipsModelJsonDeserializer.deserialize(
            json_string=json_string
        )[0]
