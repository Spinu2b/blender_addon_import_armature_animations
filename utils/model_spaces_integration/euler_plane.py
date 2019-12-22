from ...utils.model_spaces_integration.axis import Axis


class EulerPlane:
    def __init__(self, axis_a: Axis, axis_b: Axis):
        self.axis_a = axis_a
        self.axis_b = axis_b
