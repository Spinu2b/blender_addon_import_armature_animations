from ..animations_model.constructing.armature_with_animation_clips_model_builder import \
    ArmatureWithAnimationClipsModelBuilder
from ..blender_api.blender_animated_armature_constructor import BlenderAnimatedArmatureConstructor
from ..tests.animation_frame_dict_builder import AnimationFrameDictBuilder
from ..tests.rotation_builder import RotationBuilder, AngleUnit
from ..utils.model_spaces_integration.model_spaces_info import ModelSpacesInfo
from ..utils.model_spaces_integration.vector3d_basing_model_vector3d_builder import Vector3dBasingModelVector3dBuilder
from ..animations_model.model.armature_with_animation_clips_model import ArmatureWithAnimationClipsModel


class TestQuaternionRotations:
    def _get_test_armature_animation_clips_model(self) -> ArmatureWithAnimationClipsModel:
        armature_with_animation_clips_model_builder = ArmatureWithAnimationClipsModelBuilder()
        armature_with_animation_clips_model_builder\
            .add_animation_clip(animation_clip_name="TEST_ANIMATION_CLIP")\

        for angle in range(0, 360+1):
            armature_with_animation_clips_model_builder.add_frame_to_animation_clip(
                animation_clip_name="TEST_ANIMATION_CLIP",
                animation_frame_number=angle+1,
                animation_frame_dict=
                AnimationFrameDictBuilder()
                .add_node(
                    parent_name=None,
                    name="TEST_BONE",
                    rotation=
                    RotationBuilder()
                    .set_rotation_axis_and_angle(
                        axis=Vector3dBasingModelVector3dBuilder(axis_info=ModelSpacesInfo.MODEL_AXIS_INFO)
                        .forward_axis_value(value=0.0, forward_increasing=True)
                        .side_right_value(value=-1.0, side_right_increasing=True)
                        .up_axis_value(value=0.0, up_increasing=True)
                        .build(),
                        angle=angle, angle_unit=AngleUnit.DEGREES, counterclockwise=True
                    )
                    .build()
                )
                .build()
            )

        return armature_with_animation_clips_model_builder.build()

    def run(self):
        test_armature_animation_clips_model = self._get_test_armature_animation_clips_model()
        blender_animated_armature_constructor = BlenderAnimatedArmatureConstructor()
        blender_animated_armature_constructor.apply_armature_with_animation_clips_model(
            test_armature_animation_clips_model)
