from .model.animations.constructing.armature_with_animation_clips_model_loader import \
    ArmatureWithAnimationClipsModelLoader
from .model.animations.constructing.armature_with_animation_clips_model_for_test_loader import \
    ArmatureWithAnimationClipsModelForTestLoader
from .blender_api.blender_animated_rigged_model_constructor import BlenderAnimatedRiggedModelConstructor
from .model.objects.constructing.export_objects_library_model_loader import ExportObjectsLibraryModelLoader


class MainAddonLogic:
    def run(self, path_to_animations_file, path_to_objects_library_file, hierarchical=True):
        print("Running addon!")
        if hierarchical:
            return self.run_hierarchical(path_to_animations_file, path_to_objects_library_file)
        export_objects_library_model = ExportObjectsLibraryModelLoader().load(path_to_objects_library_file)
        # armature_animation_clips_model = ArmatureWithAnimationClipsModelForTestLoader().load(path_to_animations_file)

        # export_objects_library_model = ExportObjectsLibraryModelLoader().load(path_to_objects_library_file)
        armature_animation_clips_model = ArmatureWithAnimationClipsModelLoader().load(path_to_animations_file)
        print("Filtering too long animation clips")
        # armature_animation_clips_model.remove_animation_clips_longer_than(frames_count=100)
        print("Filtering done")

        animated_rigged_model_constructor = BlenderAnimatedRiggedModelConstructor()
        animated_rigged_model_constructor.build_animated_rigged_model(
            export_objects_library_model, armature_animation_clips_model)

    def run_hierarchical(self, path_to_animations_file, path_to_objects_library_file):
        # Exact mode: a hierarchical armature keyed with local transforms (keeps R3's squash & stretch shear)
        import json
        from .blender_api.blender_operations.constructing_rigged_animated_model.blender_animated_rigged_model_creator \
            import BlenderAnimatedRiggedModelCreator
        from .blender_api.blender_operations.constructing_animations.hierarchical.hierarchical_armature_animator \
            import HierarchicalArmatureAnimator
        export_objects_library_model = ExportObjectsLibraryModelLoader().load(path_to_objects_library_file)
        export_objects_library_model.reform_for_blender_building_process()
        armature_obj = BlenderAnimatedRiggedModelCreator().construct_rig(
            export_objects_library_model.get_armature_bind_pose_model(),
            export_objects_library_model.animated_export_objects)
        with open(path_to_animations_file, 'r') as animations_file:
            animation_clips_json = json.load(animations_file)['animationClips']
        from .blender_api.blender_operations.constructing_animations.hierarchical.vertex_morph_shape_keys \
            import VertexMorphShapeKeysBuilder
        with open(path_to_objects_library_file, 'r') as library_file:
            library_json = json.load(library_file)
        morphs_builder = VertexMorphShapeKeysBuilder()
        morph_properties = morphs_builder.build(armature_obj, library_json)
        animator = HierarchicalArmatureAnimator()
        animator.restructure_and_animate(armature_obj, animation_clips_json, morph_properties)
        report = animator.report_lines + morphs_builder.report_lines
        for line in report:
            print(line)
        return report
