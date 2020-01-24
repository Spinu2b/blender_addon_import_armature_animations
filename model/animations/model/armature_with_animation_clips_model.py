from typing import Dict
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ....model.animations.model.animations.animation_clip_model import AnimationClipModel


class ArmatureWithAnimationClipsModel:
    def __init__(self):
        self.animation_clips = dict()  # type: Dict[str, AnimationClipModel]

    def get_animation_clips(self) -> Dict[str, 'AnimationClipModel']:
        return self.animation_clips

    def remove_animation_clips_longer_than(self, frames_count: int):
        self.animation_clips = {animation_clip_name: self.animation_clips[animation_clip_name]
                                for animation_clip_name in self.animation_clips if
                                len(self.animation_clips[animation_clip_name].frames) <= frames_count}
