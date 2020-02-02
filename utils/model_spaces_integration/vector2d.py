

class Vector2d:
    def __init__(self, x: float, y: float):
        self.x = x  # type: float
        self.y = y  # type: float

    @classmethod
    def from_json_dict(cls, vector2d_json_dict):
        return Vector2d(float(vector2d_json_dict["x"]), float(vector2d_json_dict["y"]))
