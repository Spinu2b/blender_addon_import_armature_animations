from ..blender_api.blender_operations.general_api_operations.blender_editor_manipulation import BlenderEditorManipulation
from ..blender_api.blender_operations.constructing_animations.blender_armature_animation_constructor import \
    BlenderArmatureAnimationConstructor
from ..model.animations.model.animations.animation_frame_model import AnimationFrameModel, AnimationFrameNodeModel
from ..blender_api.blender_armature_constructor import BlenderArmatureConstructor
from ..utils.model_spaces_integration.model_spaces_info import ModelSpacesInfo
from ..utils.model_spaces_integration.rotation_builder import RotationBuilder, AngleUnit
from ..utils.model_spaces_integration.vector3d_basing_model_vector3d_builder import Vector3dBasingModelVector3dBuilder
from ..utils.model_spaces_integration.quaternion import Quaternion
from ..utils.model_spaces_integration.vector3d import Vector3d
from ..model.objects.model.export_objects_library_model_description.armature_bind_pose_model import \
    ArmatureBindPoseModel, ArmatureBindPoseModelNode


class TestArmatureBonesOrientationEditPoseModes:
    def run(self):

        bone_rotation = \
            RotationBuilder(). \
            set_rotation_axis_and_angle(
                axis=Vector3dBasingModelVector3dBuilder(axis_info=ModelSpacesInfo.BLENDER_AXIS_INFO)
                .forward_axis_value(value=0.0, forward_increasing=True)
                .side_right_value(value=-1.0, side_right_increasing=True)
                .up_axis_value(value=-1.0, up_increasing=True).build(),
                angle=30,
                angle_unit=AngleUnit.DEGREES,
                counterclockwise=True).build()

        armature_bind_pose_model = ArmatureBindPoseModel()
        armature_bind_pose_model.add_node(
            parent_key=None,
            node_key="ROOT_CHANNEL",
            node=ArmatureBindPoseModelNode(
                bone_name="ROOT_CHANNEL",
                position=Vector3d(0.0, 0.0, 0.0),
                rotation=Quaternion(1.0, 0.0, 0.0, 0.0),
                scale=Vector3d(1.0, 1.0, 1.0)
            )
        )
        armature_bind_pose_model.add_node(
            parent_key="ROOT_CHANNEL",
            node_key="Test_Channel",
            node=ArmatureBindPoseModelNode(
                bone_name="Test_Channel",
                position=Vector3d(0.0, 0.0, 0.0),
                rotation=bone_rotation,
                scale=Vector3d(1.0, 1.0, 1.0)
            )
        )

        blender_edit_mode_armature_model = armature_bind_pose_model.get_blender_edit_mode_armature_model()

        blender_armature_data_block, blender_armature_obj = BlenderArmatureConstructor().build_armature(
            blender_edit_mode_armature_model=blender_edit_mode_armature_model,
            name="TEST_ARMATURE")

        animation_frame_model = AnimationFrameModel()
        animation_frame_model.add_node(
            parent_key=None,
            node_key="ROOT_CHANNEL",
            node=AnimationFrameNodeModel(
                node_name="ROOT_CHANNEL",
                position=Vector3d(0.0, 0.0, 0.0),
                rotation=Quaternion(1.0, 0.0, 0.0, 0.0),
                scale=Vector3d(1.0, 1.0, 1.0),
                local_position=Vector3d(0.0, 0.0, 0.0),
                local_rotation=Quaternion(1.0, 0.0, 0.0, 0.0),
                local_scale=Vector3d(1.0, 1.0, 1.0)
            )
        )
        animation_frame_model.add_node(
            parent_key="ROOT_CHANNEL",
            node_key="Test_Channel",
            node=AnimationFrameNodeModel(
                node_name="Test_Channel",
                position=Vector3d(0.0, 0.0, 0.0),
                rotation=bone_rotation,
                scale=Vector3d(1.0, 1.0, 1.0),
                local_position=Vector3d(0.0, 0.0, 0.0),
                local_rotation=Quaternion(1.0, 0.0, 0.0, 0.0),
                local_scale=Vector3d(1.0, 1.0, 1.0)
            )
        )

        blender_pose_mode_animation_frame_model = animation_frame_model.get_blender_pose_mode_animation_frame_model(
            armature_bind_pose_model
        )

        blender_editor_manipulation = BlenderEditorManipulation()
        blender_editor_manipulation.enter_pose_mode()

        BlenderArmatureAnimationConstructor().setup_keyframe_in_animation_clip(
            blender_pose_mode_animation_frame_model,
            blender_armature_obj
        )
