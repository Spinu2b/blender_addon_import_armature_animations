from math import sqrt


class Quaternion:
    def __init__(self, w: float = 1.0, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.w = w  # type: float
        self.x = x  # type: float
        self.y = y  # type: float
        self.z = z  # type: float

    def conjugate(self):
        return Quaternion(
            w=self.w,
            x=-self.x,
            y=-self.y,
            z=-self.z)

    def inverse(self):
        denominator = self.w**2 + self.x**2 + self.y**2 + self.z**2
        quaternion_conjugate = self.conjugate()

        return Quaternion(
            w=quaternion_conjugate.w / denominator,
            x=quaternion_conjugate.x / denominator,
            y=quaternion_conjugate.y / denominator,
            z=quaternion_conjugate.z / denominator)

    def magnitude(self) -> float:
        return sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)

    def normalized(self):
        quaternion_magnitude = self.magnitude()

        return Quaternion(
            w=self.w / quaternion_magnitude,
            x=self.x / quaternion_magnitude,
            y=self.y / quaternion_magnitude,
            z=self.z / quaternion_magnitude
        )

    @classmethod
    def from_json_dict(cls, quaternion_json_dict):
        return Quaternion(
            w=float(quaternion_json_dict["w"]),
            x=float(quaternion_json_dict["x"]),
            y=float(quaternion_json_dict["y"]),
            z=float(quaternion_json_dict["z"])
        )
