from typing import List

from ...utils.model_spaces_integration.vector3d import Vector3d


class MatrixMultiplicator:
    def multiply(self, matrix_a: List[List[float]], matrix_b: List[List[float]]) -> List[List[float]]:
        n = len(matrix_a)
        m = len(matrix_a[0])
        p = len(matrix_b[0])

        result = [[0.0 for x in range(p)] for y in range(n)]

        for i in range(n):
            for j in range(p):
                result[i][j] = sum(matrix_a[i][r] * matrix_b[r][j] for r in range(m))

        return result


class Matrix3x3:
    def __init__(self,
                 a: float = 0.0,
                 b: float = 0.0,
                 c: float = 0.0,
                 d: float = 0.0,
                 e: float = 0.0,
                 f: float = 0.0,
                 g: float = 0.0,
                 h: float = 0.0,
                 i: float = 0.0):
        self.elements = [[a, b, c], [d, e, f], [g, h, i]]  # type: List[List[float]]

    def multiply_to_vector(self, vector: Vector3d) -> Vector3d:
        return Vector3d.from_matrix_elements(MatrixMultiplicator().multiply(
            self.elements, vector.to_matrix_elements()))
