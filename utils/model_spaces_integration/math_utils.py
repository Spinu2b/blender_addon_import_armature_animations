from ...utils.model_spaces_integration.vector3d import Vector3d


class MathUtils:
    @classmethod
    def is_close_enough_to_zero(cls, value: float) -> bool:
        margin = 0.000001
        return abs(value) < margin

    @classmethod
    def get_scale_ratio_vector3d(cls, scale_a: Vector3d, scale_b: Vector3d) -> Vector3d:
        raise NotImplementedError
