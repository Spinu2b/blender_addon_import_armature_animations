from ...utils.model_spaces_integration.axis import Axis
from ...utils.model_spaces_integration.axis_direction import AxisDirection


class AxisInfo:
    def __init__(self,
                 forward_axis: Axis,
                 up_axis: Axis,
                 side_axis: Axis,
                 right_direction_values: AxisDirection,
                 forward_direction_values: AxisDirection,
                 up_direction_values: AxisDirection):
        self.forward_axis = forward_axis  # type: Axis
        self.up_axis = up_axis  # type: Axis
        self.side_axis = side_axis  # type: Axis
        self.right_direction_values = right_direction_values  # type: AxisDirection
        self.forward_direction_values = forward_direction_values  # type: AxisDirection
        self.up_direction_values = up_direction_values  # type: AxisDirection
