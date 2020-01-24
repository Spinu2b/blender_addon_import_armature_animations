from .....utils.model_spaces_integration.axis_info import AxisInfo


class BoneBindPose:
    def translate_to_space_model(self, base_space_model: AxisInfo, target_space_model: AxisInfo):
        raise NotImplementedError
