from blender_api.blender_operations.constructing_rigged_animated_model.blender_animated_rigged_model_creator import \
    BlenderAnimatedRiggedModelCreator
from model.animations.model.armature_with_animation_clips_model import ArmatureWithAnimationClipsModel
from model.objects.model.export_objects_library_model import ExportObjectsLibraryModel


class BlenderAnimatedRiggedModelConstructor:
    def build_animated_rigged_model(
            self, export_objects_library_model: ExportObjectsLibraryModel,
            armature_animation_clips_model: ArmatureWithAnimationClipsModel):
        armature_bind_pose_model = export_objects_library_model.get_armature_bind_pose_model()
        # type: ArmatureBindPoseModel
        armature_animation_clips_model = armature_animation_clips_model.\
            filter_to_only_animation_clips_matching_armature(export_objects_library_model.armature_hierarchy)
        # type: ArmatureWithAnimationClipsModel

        BlenderAnimatedRiggedModelCreator().construct_using(
            armature_bind_pose_model=armature_bind_pose_model,
            animated_export_objects=export_objects_library_model.animated_export_objects,
            armature_animation_clips_model=armature_animation_clips_model
        )
