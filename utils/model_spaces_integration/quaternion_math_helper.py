from ...utils.model_spaces_integration.vector3d import Vector3d
from ...utils.model_spaces_integration.quaternion import Quaternion


class QuaternionManipulator:
    @classmethod
    def multiply(cls, quaternion_a: Quaternion, quaternion_b: Quaternion) -> Quaternion:
        a = quaternion_a.w
        b = quaternion_a.x
        c = quaternion_a.y
        d = quaternion_a.z
        e = quaternion_b.w
        f = quaternion_b.x
        g = quaternion_b.y
        h = quaternion_b.z

        return Quaternion(
            w=a*e - b*f - c*g - d*h,
            x=b*e + a*f + c*h - d*g,
            y=a*g - b*h + c*e + d*f,
            z=a*h + b*g - c*f + d*e
        )


class QuaternionMathHelper:
    @classmethod
    def get_zero_relative_rotation_quaternion(cls) -> Quaternion:
        return Quaternion(1.0, 0.0, 0.0, 0.0)

    @classmethod
    def derive_local_quaternion_rotation(cls,
                                         child_absolute_rotation: Quaternion,
                                         parent_absolute_rotation: Quaternion) -> Quaternion:
        relative = QuaternionManipulator.multiply(parent_absolute_rotation.inverse(),
                                                  child_absolute_rotation)
        return relative

    @classmethod
    def subtract_relative_rotation(cls,
                                   absolute_base: Quaternion,
                                   relative_rotation: Quaternion) -> Quaternion:
        return QuaternionManipulator.multiply(absolute_base, relative_rotation.inverse())

    @classmethod
    def add_absolute_rotation(cls,
                              relative_base: Quaternion,
                              absolute_rotation: Quaternion) -> Quaternion:
        return QuaternionManipulator.multiply(relative_base, absolute_rotation)

    @classmethod
    def rotate_vector_by(cls, vector: Vector3d, rotation: Quaternion) -> Vector3d:
        result = QuaternionManipulator.multiply(
            quaternion_a=QuaternionManipulator.multiply(
                quaternion_a=rotation,
                quaternion_b=Quaternion(
                    w=0,
                    x=vector.x,
                    y=vector.y,
                    z=vector.z
                )
            ),
            quaternion_b=rotation.inverse()
        )

        return Vector3d(
            x=result.x,
            y=result.y,
            z=result.z
        )
