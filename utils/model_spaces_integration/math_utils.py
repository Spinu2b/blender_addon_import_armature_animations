

class MathUtils:
    @classmethod
    def is_close_enough_to_zero(cls, value: float) -> bool:
        margin = 0.000001
        return abs(value) < margin
