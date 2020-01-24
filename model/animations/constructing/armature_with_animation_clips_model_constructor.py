from ....model.animations.constructing.armature_with_animation_clips_model_builder import\
    ArmatureWithAnimationClipsModelBuilder


class ArmatureWithAnimationClipsModelConstructor:
    def construct_from_json(self, json_dict):
        result_builder = ArmatureWithAnimationClipsModelBuilder()
        for animation_clip_name in json_dict["animationClips"]:
            result_builder.add_animation_clip(animation_clip_name)
            for animation_frame_number in json_dict["animationClips"][animation_clip_name]:
                animation_frame_dict = json_dict["animationClips"][animation_clip_name][animation_frame_number]
                result_builder.add_frame_to_animation_clip(animation_clip_name, animation_frame_dict,
                                                           int(animation_frame_number) + 1)
        return result_builder.build()
