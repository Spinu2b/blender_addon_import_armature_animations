from .animations_model.constructing.armature_with_animation_clips_model_loader import ArmatureWithAnimationClipsModelLoader
from .blender_api.blender_animated_armature_constructor import BlenderAnimatedArmatureConstructor


class MainAddonLogic:
    def run(self):
        path_to_file = "D:/exported_rayman_animations.json"
        armature_animation_clips_model = ArmatureWithAnimationClipsModelLoader().load(path_to_file)
        blender_animated_armature_constructor = BlenderAnimatedArmatureConstructor()
        blender_animated_armature_constructor.apply_armature_with_animation_clips_model(armature_animation_clips_model)
