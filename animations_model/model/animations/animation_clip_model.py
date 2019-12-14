from typing import Dict

from animations_model.model.animations.animation_frame_model import AnimationFrameModel


class AnimationClipModel:
    def __init__(self, animation_clip_name: str):
        self.animation_clip_name = animation_clip_name  # type: str
        self.frames = dict()  # type: Dict[int, AnimationFrameModel]

    def get_first_animation_frame(self) -> AnimationFrameModel:
        minimal_key = min(self.frames)  # type: int
        return self.frames[minimal_key]
