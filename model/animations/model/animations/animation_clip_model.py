from typing import Dict

from .....utils.model_spaces_integration.axis_info import AxisInfo
from .....model.animations.model.animations.animation_frame_model import AnimationFrameModel


class AnimationClipModel:
    def __init__(self, animation_clip_name: str):
        self.animation_clip_name = animation_clip_name  # type: str
        self.frames = dict()  # type: Dict[int, AnimationFrameModel]

    def get_first_animation_frame(self) -> 'AnimationFrameModel':
        minimal_key = min(self.frames)  # type: int
        return self.frames[minimal_key]

    def get_animation_frames(self) -> Dict[int, 'AnimationFrameModel']:
        return self.frames

    def translate_to_space_model(self, base_space_model: AxisInfo, target_space_model: AxisInfo):
        for frame_number in self.frames:
            self.frames[frame_number].\
                translate_to_space_model(base_space_model=base_space_model, target_space_model=target_space_model)
