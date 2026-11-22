"""Matrix helpers for the hierarchical (exact) import of Raymap animations.

Raymap (Unity) composes a channel's world matrix as parentWorld @ T @ R @ S from the channel's local TRS, with the
frame's own parent. With non-uniform scales this produces shear in the children, which a single bone's
location / rotation / scale cannot hold, but a hierarchy of bones with full scale inheritance reproduces exactly.
"""
import numpy as np

# Unity (x, y, z) -> Blender (-x, -z, y): the axis mapping used by the rest of the addon.
UNITY_TO_BLENDER = np.array([[-1.0, 0.0, 0.0, 0.0],
                             [0.0, 0.0, -1.0, 0.0],
                             [0.0, 1.0, 0.0, 0.0],
                             [0.0, 0.0, 0.0, 1.0]])
BLENDER_TO_UNITY = np.linalg.inv(UNITY_TO_BLENDER)
# The bone-local turn the addon's rest bones carry (180 degrees about Z); verified against the existing importer:
# a bone's armature-space pose matrix == UNITY_TO_BLENDER @ W_unity @ BLENDER_TO_UNITY @ BONE_LOCAL_TURN.
BONE_LOCAL_TURN = np.diag([-1.0, -1.0, 1.0, 1.0])
BONE_LOCAL_TURN_INVERSE = np.linalg.inv(BONE_LOCAL_TURN)

HIDDEN_BONE_SCALE = 0.0001
COLUMNS_ORTHOGONALITY_EPSILON = 1e-4


def quaternion_dict_to_matrix3(q) -> np.ndarray:
    w, x, y, z = q['w'], q['x'], q['y'], q['z']
    n = (w * w + x * x + y * y + z * z) ** 0.5 or 1.0
    w, x, y, z = w / n, x / n, y / n, z / n
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def local_trs_matrix_of_frame_node(node) -> np.ndarray:
    result = np.eye(4)
    result[:3, :3] = quaternion_dict_to_matrix3(node['localRotation']) @ np.diag(
        [node['localScale']['x'], node['localScale']['y'], node['localScale']['z']])
    result[:3, 3] = [node['localPosition']['x'], node['localPosition']['y'], node['localPosition']['z']]
    return result


def frame_unity_world_and_local_matrices_and_parents(frame_json):
    """Per channel name: (world matrix, local matrix, frame parent name), composed in the frame's own hierarchy."""
    result = {}

    def walk(tree_node, parent_world, parent_name):
        local = local_trs_matrix_of_frame_node(tree_node['Node'])
        world = parent_world @ local
        result[tree_node['Id']] = (world, local, parent_name)
        for child in tree_node['Children']:
            walk(child, world, tree_node['Id'])

    walk(frame_json['Root'], np.eye(4), None)
    return result


def unity_world_to_blender_armature_pose(unity_world: np.ndarray) -> np.ndarray:
    return UNITY_TO_BLENDER @ unity_world @ BLENDER_TO_UNITY @ BONE_LOCAL_TURN


def unity_local_to_blender_bone_basis(unity_local: np.ndarray) -> np.ndarray:
    # parent pose^-1 @ child pose for parent/child poses produced by unity_world_to_blender_armature_pose
    return BONE_LOCAL_TURN_INVERSE @ UNITY_TO_BLENDER @ unity_local @ BLENDER_TO_UNITY @ BONE_LOCAL_TURN


def columns_orthogonality_residual(matrix3: np.ndarray) -> float:
    """0 when the matrix is rotation @ diagonal scale (representable as one bone's rotation + scale)."""
    norms = np.linalg.norm(matrix3, axis=0)
    if np.any(norms < 1e-12):
        return 0.0
    normalized = matrix3 / norms
    return float(np.abs(normalized.T @ normalized - np.eye(3)).max())


def decompose_trs(matrix4: np.ndarray):
    """matrix4 ~ T @ R @ S -> (translation, rotation matrix3, scale vector). Exact when the columns are orthogonal."""
    translation = matrix4[:3, 3].copy()
    a = matrix4[:3, :3]
    scale = np.linalg.norm(a, axis=0)
    scale = np.where(scale < 1e-12, 1e-12, scale)
    rotation = a / scale
    if np.linalg.det(rotation) < 0:
        scale[0] = -scale[0]
        rotation[:, 0] = -rotation[:, 0]
    u, _, vt = np.linalg.svd(rotation)  # re-orthonormalize against float noise
    rotation = u @ vt
    return translation, rotation, scale


def compose_trs(translation, rotation3, scale) -> np.ndarray:
    result = np.eye(4)
    result[:3, :3] = rotation3 @ np.diag(scale)
    result[:3, 3] = translation
    return result


_SIGNED_PERMUTATIONS = []
for _permutation in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)):
    for _signs in ((1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1), (-1, 1, 1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1)):
        _m = np.zeros((3, 3))
        for _column, (_row, _sign) in enumerate(zip(_permutation, _signs)):
            _m[_row, _column] = _sign
        _SIGNED_PERMUTATIONS.append(_m)


def aligned_svd(matrix3: np.ndarray, previous_u, previous_vt):
    """matrix3 = U @ diag(sigma) @ Vt with U, Vt proper rotations (a reflection goes into a negative sigma),
    choosing among the equivalent orderings / signs the one closest to the previous frame's (for smooth keys)."""
    u, sigma, vt = np.linalg.svd(matrix3)
    best = None
    for p in _SIGNED_PERMUTATIONS:
        u2 = u @ p
        vt2 = p.T @ vt
        sigma2 = np.diag(p.T @ np.diag(sigma) @ p).copy()
        # p.T diag p is diagonal again for a signed permutation; fix determinants by moving signs into sigma
        if np.linalg.det(u2) < 0:
            u2 = u2.copy(); u2[:, 0] = -u2[:, 0]; sigma2[0] = -sigma2[0]
        if np.linalg.det(vt2) < 0:
            vt2 = vt2.copy(); vt2[0, :] = -vt2[0, :]; sigma2[0] = -sigma2[0]
        if previous_u is None:
            cost = np.abs(u2 - np.eye(3)).sum() + np.abs(vt2 - np.eye(3)).sum()
        else:
            cost = np.abs(u2 - previous_u).sum() + np.abs(vt2 - previous_vt).sum()
        if best is None or cost < best[0]:
            best = (cost, u2, sigma2, vt2)
    return best[1], best[2], best[3]
