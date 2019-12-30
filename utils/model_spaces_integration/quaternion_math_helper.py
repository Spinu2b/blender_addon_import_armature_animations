import copy

try:
    from ...utils.model_spaces_integration.vector3d import Vector3d
    from ...utils.model_spaces_integration.quaternion import Quaternion
except ValueError:
    from utils.model_spaces_integration.vector3d import Vector3d
    from utils.model_spaces_integration.quaternion import Quaternion


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

        return cls._zero_out_too_small_coefficients(Quaternion(
            w=a*e - b*f - c*g - d*h,
            x=b*e + a*f + c*h - d*g,
            y=a*g - b*h + c*e + d*f,
            z=a*h + b*g - c*f + d*e
        ))

    @classmethod
    def _zero_out_too_small_coefficients(cls, quaternion: Quaternion) -> Quaternion:
        margin = 0.0000001
        result = copy.deepcopy(quaternion)
        result.w = result.w if abs(result.w) > margin else 0.0
        result.x = result.x if abs(result.x) > margin else 0.0
        result.y = result.y if abs(result.y) > margin else 0.0
        result.z = result.z if abs(result.z) > margin else 0.0
        return result

    @classmethod
    def is_equal(cls, quaternion_a: Quaternion, quaternion_b: Quaternion) -> bool:
        margin = 0.0000001
        return abs(quaternion_a.w - quaternion_b.w) < margin and \
            abs(quaternion_a.x - quaternion_b.x) < margin and \
            abs(quaternion_a.y - quaternion_b.y) < margin and \
            abs(quaternion_a.z - quaternion_b.z) < margin


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
