from blender_api.blender_armature_constructor import BlenderArmatureConstructor


class BlenderAnimatedArmatureConstructor:
    def apply_armature_with_animation_clips_model(self, armature_animation_clips_model):
        unified_armature_model = armature_animation_clips_model.get_unified_armature_model()
        blender_armature_constructor = BlenderArmatureConstructor()
        blender_armature = blender_armature_constructor.build_armature(unified_armature_model)
        for animation_clip in armature_animation_clips_model.get_animation_clips():
            for animation_frame in animation_clip.get_animation_frames():
                self.add_animation_frame_to_animation_clip_of_armature(
                    blender_armature,
                    animation_clip.name,
                    animation_frame.index,
                    animation_frame)

    def add_animation_frame_to_animation_clip_of_armature(self, blender_armature, animation_clip_name,
                                                          animation_frame_number, animation_frame_model):
        pass
