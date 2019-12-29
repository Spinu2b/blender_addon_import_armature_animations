from typing import List


class Vector3d:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x  # type: float
        self.y = y  # type: float
        self.z = z  # type: float

    def __add__(self, other):
        return Vector3d(
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z
        )

    def __sub__(self, other):
        return Vector3d(
            x=self.x - other.x,
            y=self.y - other.y,
            z=self.z - other.z
        )

    def __floordiv__(self, other: float):
        return Vector3d(
            x=self.x // other,
            y=self.y // other,
            z=self.z // other
        )

    def __truediv__(self, other: float):
        return Vector3d(
            x=self.x / other,
            y=self.y / other,
            z=self.z / other
        )

    def __neg__(self):
        return Vector3d(
            x=-self.x,
            y=-self.y,
            z=-self.z
        )

    def to_matrix_elements(self) -> List[List[float]]:
        return [[self.x], [self.y], [self.z]]

    @classmethod
    def from_matrix_elements(cls, matrix_elements: List[List[float]]):
        columns = len(matrix_elements[0])
        rows = len(matrix_elements)

        if columns != 1 or rows != 3:
            raise ValueError("Invalid size of matrix to convert to Vector3d! {} x {}".format(rows, columns))

        return Vector3d(x=matrix_elements[0][0], y=matrix_elements[1][0], z=matrix_elements[2][0])
