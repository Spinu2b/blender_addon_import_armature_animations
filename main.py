from .blender_api.blender_animated_rigged_model_constructor import BlenderAnimatedRiggedModelConstructor
from .model.animations.constructing.armature_with_animation_clips_model_loader import \
    ArmatureWithAnimationClipsModelLoader
from .model.objects.constructing.export_objects_library_model_loader import ExportObjectsLibraryModelLoader


class MainAddonLogic:
    def run(self):
        print("Running addon!")
        path_to_animations_file = "D:/exported_rayman_animations.json"
        path_to_objects_library_file = "D:/exported_rayman_meshes.json"
        export_objects_library_model = ExportObjectsLibraryModelLoader().load(path_to_objects_library_file)
        armature_animation_clips_model = ArmatureWithAnimationClipsModelLoader().load(path_to_animations_file)
        print("Filtering too long animation clips")
        armature_animation_clips_model.remove_animation_clips_longer_than(frames_count=100)
        print("Filtering done")

        animated_rigged_model_constructor = BlenderAnimatedRiggedModelConstructor()
        animated_rigged_model_constructor.build_animated_rigged_model(
            export_objects_library_model, armature_animation_clips_model)
