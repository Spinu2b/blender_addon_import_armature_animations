from typing import List, Tuple, Dict

from utils.model_spaces_integration.vector3d import Vector3d


class MeshGeometry:
    def __init__(self):
        self.vertices = []  # type: List[Vector3d]
        self.triangles = []  # type: List[Tuple[int, int, int]]
        self.bones_weights = dict()  # type: Dict[str, Dict[int, float]]
