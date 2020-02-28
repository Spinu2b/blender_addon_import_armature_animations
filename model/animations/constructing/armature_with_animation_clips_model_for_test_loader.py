import json
import orjson

from ....model.animations.constructing.armature_with_animation_clips_model_constructor import \
    ArmatureWithAnimationClipsModelConstructor
from ....model.animations.model.armature_with_animation_clips_model import ArmatureWithAnimationClipsModel


class ArmatureWithAnimationClipsModelForTestLoader:
    ANIMATION_CLIPS_COUNT = 2

    def load(self, path_to_json_file: str) -> 'ArmatureWithAnimationClipsModel':
        with open(path_to_json_file, 'r') as json_file:
            json_dict = orjson.loads(json_file.read())
        json_dict = self._reduce_amount_of_json_dict_data(json_dict)
        return ArmatureWithAnimationClipsModelConstructor().construct_from_json(json_dict)

    def _reduce_amount_of_json_dict_data(self, json_dict):
        result = {"animationClips": {str(animation_clip_index): json_dict["animationClips"]["Animation {}".format(
            animation_clip_index)] for animation_clip_index in range(self.ANIMATION_CLIPS_COUNT)}}
        return result
