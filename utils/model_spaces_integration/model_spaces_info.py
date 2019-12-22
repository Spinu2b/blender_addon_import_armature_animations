from utils.model_spaces_integration.axis import Axis
from utils.model_spaces_integration.axis_direction import AxisDirection
from utils.model_spaces_integration.axis_info import AxisInfo


class ModelSpacesInfo:
    MODEL_AXIS_INFO = \
        AxisInfo(
            forward_axis=Axis.Z,
            up_axis=Axis.Y,
            side_axis=Axis.X,
            right_direction_values=AxisDirection.INCREASING_VALUES,
            forward_direction_values=AxisDirection.INCREASING_VALUES,
            up_direction_values=AxisDirection.INCREASING_VALUES
        )

    BLENDER_AXIS_INFO =\
        AxisInfo(
            forward_axis=Axis.Y,
            up_axis=Axis.Z,
            side_axis=Axis.X,
            right_direction_values=AxisDirection.DECREASING_VALUES,
            forward_direction_values=AxisDirection.DECREASING_VALUES,
            up_direction_values=AxisDirection.INCREASING_VALUES
        )
