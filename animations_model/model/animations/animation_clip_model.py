
class AnimationClipModel:
    def __init__(self, animation_clip_name):
        self.animation_clip_name = animation_clip_name
        self.frames = dict()

    def get_first_animation_frame(self):
        minimal_key = min(self.frames)
        return self.frames[minimal_key]
