from .animations_model.constructing.armature_with_animation_clips_model_loader import\
    ArmatureWithAnimationClipsModelLoader
from .blender_api.blender_animated_armature_constructor import BlenderAnimatedArmatureConstructor


class MainAddonLogic:
    def run(self):
        print("Running addon!")
        path_to_file = "D:/exported_rayman_animations.json"
        armature_animation_clips_model = ArmatureWithAnimationClipsModelLoader().load(path_to_file)
        print("Filtering too long animation clips")
        armature_animation_clips_model.remove_animation_clips_longer_than(frames_count=250)
        print("Filtering done")
        blender_animated_armature_constructor = BlenderAnimatedArmatureConstructor()
        blender_animated_armature_constructor.apply_armature_with_animation_clips_model(armature_animation_clips_model)
