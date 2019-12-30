try:
    from ..utils.model_spaces_integration.quaternion import Quaternion
    from ..utils.model_spaces_integration.quaternion_math_helper import QuaternionManipulator
    from ..utils.model_spaces_integration.rotation_builder import RotationBuilder, AngleUnit
    from ..utils.model_spaces_integration.model_spaces_info import ModelSpacesInfo
    from ..utils.model_spaces_integration.vector3d_basing_model_vector3d_builder import\
        Vector3dBasingModelVector3dBuilder
except SystemError:
    from utils.model_spaces_integration.quaternion import Quaternion
    from utils.model_spaces_integration.quaternion_math_helper import QuaternionManipulator
    from utils.model_spaces_integration.rotation_builder import RotationBuilder, AngleUnit
    from utils.model_spaces_integration.model_spaces_info import ModelSpacesInfo
    from utils.model_spaces_integration.vector3d_basing_model_vector3d_builder import\
        Vector3dBasingModelVector3dBuilder


class TestQuaternionManipulator:
    def test_multiply_inverse(self):
        quaternion_a = Quaternion(1., 2., 3., 4.).normalized()
        quaternion_b = quaternion_a.inverse()

        result = QuaternionManipulator.multiply(quaternion_a, quaternion_b)
        assert QuaternionManipulator.is_equal(result, Quaternion(1.0, 0.0, 0.0, 0.0))

    def test_multiply_full_angle(self):
        identity_quaternion = Quaternion(1.0, 0.0, 0.0, 0.0)
        for angle in range(0, 360 + 1):
            rotation = RotationBuilder()\
                .set_rotation_axis_and_angle(
                axis=Vector3dBasingModelVector3dBuilder(axis_info=ModelSpacesInfo.MODEL_AXIS_INFO)
                    .forward_axis_value(value=0.0, forward_increasing=True)
                    .side_right_value(value=-1.0, side_right_increasing=True)
                    .up_axis_value(value=0.0, up_increasing=True)
                    .build(),
                    angle=angle, angle_unit=AngleUnit.DEGREES, counterclockwise=True
                )\
                .build()
            assert QuaternionManipulator.is_equal(QuaternionManipulator.multiply(rotation, rotation.inverse()),
                                                  identity_quaternion)
