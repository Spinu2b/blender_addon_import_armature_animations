from ...utils.model_spaces_integration.quaternion import Quaternion


class QuaternionMathHelper:
    @classmethod
    def get_zero_relative_rotation_quaternion(cls) -> Quaternion:
        raise NotImplementedError

    @classmethod
    def derive_local_quaternion_rotation(cls,
                                         child_absolute_rotation: Quaternion,
                                         parent_absolute_rotation: Quaternion) -> Quaternion:
        raise NotImplementedError

    @classmethod
    def subtract_relative_rotation(cls,
                                   absolute_base: Quaternion,
                                   relative_rotation: Quaternion) -> Quaternion:
        raise NotImplementedError

    @classmethod
    def add_absolute_rotation(cls,
                              relative_base: Quaternion,
                              absolute_rotation: Quaternion) -> Quaternion:
        raise NotImplementedError
