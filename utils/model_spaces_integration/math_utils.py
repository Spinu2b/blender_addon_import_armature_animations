from ...utils.model_spaces_integration.vector3d import Vector3d


class MathUtils:
    @classmethod
    def get_scale_ratio_vector3d(cls, scale_a: Vector3d, scale_b: Vector3d) -> Vector3d:
        margin = 0.000001

        result = Vector3d()

        if abs(scale_b.x) < margin:
            result.x = 0.0
        else:
            result.x = scale_a.x / scale_b.x

        if abs(scale_b.y) < margin:
            result.y = 0.0
        else:
            result.y = scale_a.y / scale_b.y

        if abs(scale_b.z) < margin:
            result.z = 0.0
        else:
            result.z = scale_a.z / scale_b.z

        return result
