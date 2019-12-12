from blender_api.blender_operations.constructing_animations.blender_armature_bone_pose_phase_manipulator import \
    BlenderArmatureBonePosePhaseManipulator


class BlenderArmatureBonePoseSetterFacade:
    def position_bone_in_animation_frame(self, animation_frame_armature_bone_model):
        blender_armature_bone_pose_phase_manipulator = BlenderArmatureBonePosePhaseManipulator()
