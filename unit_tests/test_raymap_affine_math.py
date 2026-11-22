try:
    from ..blender_api.blender_operations.constructing_animations.hierarchical.raymap_affine_math import (
        decompose_trs, compose_trs, aligned_svd, columns_orthogonality_residual)
except (SystemError, ImportError):
    from blender_api.blender_operations.constructing_animations.hierarchical.raymap_affine_math import (
        decompose_trs, compose_trs, aligned_svd, columns_orthogonality_residual)
import numpy as np


def _rotation(axis, angle):
    axis = np.asarray(axis, dtype=float) / np.linalg.norm(axis)
    k = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(angle) * k + (1 - np.cos(angle)) * k @ k


class TestRaymapAffineMath:
    def test_trs_round_trip(self):
        matrix = compose_trs([1.0, -2.0, 0.5], _rotation([1, 2, 3], 0.7), [1.0, 0.281, 1.9])
        assert columns_orthogonality_residual(matrix[:3, :3]) < 1e-9
        assert np.allclose(compose_trs(*decompose_trs(matrix)), matrix)

    def test_child_of_squashed_parent_is_sheared_and_svd_splits_it_into_two_bones(self):
        parent = compose_trs([0, 0, 0], _rotation([0, 0, 1], 0.3), [1.0, 0.281, 1.0])  # squash
        child = compose_trs([0.2, 0.5, 0], _rotation([0, 1, 1], 0.9), [1.0, 1.0, 1.0])
        world = parent @ child
        assert columns_orthogonality_residual(world[:3, :3]) > 0.1  # one bone cannot hold this
        u, sigma, vt = aligned_svd(world[:3, :3], None, None)
        assert np.linalg.det(u) > 0 and np.linalg.det(vt) > 0
        helper = compose_trs(world[:3, 3], u, sigma)  # translation + rotation + scale
        bone = np.eye(4); bone[:3, :3] = vt           # rotation only
        assert np.allclose(helper @ bone, world)

    def test_aligned_svd_stays_close_to_previous_frame(self):
        a = compose_trs([0, 0, 0], _rotation([1, 0, 0], 0.4), [2.0, 1.0, 0.5]) @ \
            compose_trs([0, 0, 0], _rotation([0, 1, 0], 0.6), [1.0, 1.0, 1.0])
        b = compose_trs([0, 0, 0], _rotation([1, 0, 0], 0.41), [2.0, 1.0, 0.5]) @ \
            compose_trs([0, 0, 0], _rotation([0, 1, 0], 0.6), [1.0, 1.0, 1.0])
        u1, s1, vt1 = aligned_svd(a[:3, :3], None, None)
        u2, s2, vt2 = aligned_svd(b[:3, :3], u1, vt1)
        assert np.abs(u2 - u1).max() < 0.05 and np.abs(vt2 - vt1).max() < 0.05
        assert np.allclose(u2 @ np.diag(s2) @ vt2, b[:3, :3])
