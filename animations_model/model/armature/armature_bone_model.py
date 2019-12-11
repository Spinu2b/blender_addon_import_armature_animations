
class ArmatureBoneModel:
    def __init__(self, bone_name,
                 position_x,
                 position_y,
                 position_z,
                 rotation_x,
                 rotation_y,
                 rotation_z,
                 scale_x,
                 scale_y,
                 scale_z):
        self.bone_name = bone_name
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z
        self.rotation_x = rotation_x
        self.rotation_y = rotation_y
        self.rotation_z = rotation_z
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.scale_z = scale_z
