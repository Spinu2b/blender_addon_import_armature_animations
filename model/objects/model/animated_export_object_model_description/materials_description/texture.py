from typing import List


class Color:
    def __init__(self, red: float, green: float, blue: float, alpha: float):
        self.red = red  # type: float
        self.green = green  # type: float
        self.blue = blue  # type: float
        self.alpha = alpha  # type: float


class Texture:
    def __init__(self):
        self.name = ""  # type: str
        self.width = 0  # type: int
        self.height = 0  # type: int
        self.pixels = []  # type: List[Color]
