from ....model.animations.json_parsing.armature_with_animation_clips_model_json_deserializer import \
    ArmatureWithAnimationClipsModelJsonDeserializer
from ....model.animations.model.armature_with_animation_clips_model import ArmatureWithAnimationClipsModel


class ArmatureWithAnimationClipsModelLoader:
    def load(cls, path_to_json_file: str) -> 'ArmatureWithAnimationClipsModel':
        with open(path_to_json_file, 'r') as json_file:
            json_string = json_file.read()
            json_string = ''.join(json_string.split())
        return ArmatureWithAnimationClipsModelJsonDeserializer.deserialize(
            json_string=json_string
        )[0]
