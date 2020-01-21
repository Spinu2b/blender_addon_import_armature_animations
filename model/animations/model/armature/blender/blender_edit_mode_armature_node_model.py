
class BlenderEditModeArmatureNodeModel:
    def __init__(self,
                 name: str,
                 head_position_x: float, head_position_y: float, head_position_z: float,
                 tail_position_x: float, tail_position_y: float, tail_position_z: float):
        self.name = name  # type: str
        self.head_position_x = head_position_x  # type: float
        self.head_position_y = head_position_y  # type: float
        self.head_position_z = head_position_z  # type: float
        self.tail_position_x = tail_position_x  # type: float
        self.tail_position_y = tail_position_y  # type: float
        self.tail_position_z = tail_position_z  # type: float
