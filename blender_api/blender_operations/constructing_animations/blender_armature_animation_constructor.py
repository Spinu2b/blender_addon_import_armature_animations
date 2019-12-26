from typing import TYPE_CHECKING
from bpy.types import Armature

from blender_api.blender_operations.general_api_operations.blender_editor_manipulation import BlenderEditorManipulation
from blender_api.blender_operations.general_api_operations.blender_objects_manipulation import \
    BlenderObjectsManipulation
from ....blender_api.blender_operations.constructing_animations.blender_armature_bone_pose_setter_facade import \
    BlenderArmatureBonePoseSetterFacade

if TYPE_CHECKING:
    from ....animations_model.model.blender_poses.blender_consolidated_pose_mode_animation_frame_model import \
        BlenderConsolidatedPoseModeAnimationFrameModel


class BlenderArmatureAnimationConstructor:
    def setup_keyframe_in_animation_clip(
            self,
            animation_frame_model: 'BlenderConsolidatedPoseModeAnimationFrameModel',
            armature: Armature):
        blender_armature_bone_pose_facade = BlenderArmatureBonePoseSetterFacade()
        blender_objects_manipulation = BlenderObjectsManipulation()
        for animation_frame_armature_bone_model in animation_frame_model.iterate_bones():
            blender_armature_bone_pose_facade.position_bone_in_animation_frame(
                armature,
                animation_frame_armature_bone_model
            )
        blender_objects_manipulation.deselect_all_objects()
        blender_armature_bone_pose_facade.select_all_pose_bones()
        blender_armature_bone_pose_facade.lock_rotation_scale_position()
