from utils.model_spaces_integration.vector3d import Vector3d


class BlenderEditModeBone:
    def __init__(self, head_position: Vector3d, tail_position: Vector3d):
        self.head_position = head_position  # type: Vector3d
        self.tail_position = tail_position  # type: Vector3d

    def position_using_bone_center(self, center_position: Vector3d):
        pass

    def scale_as_if_inside_bounding_box(self, absolute_scale: Vector3d):
        # Treat bone as if it was a diagonal of imaginary bounding box in order
        # to take into account all of three spatial scaling
        # factors - x, y and z
        pass

    def rotate_using_euler_angles(self, absolute_euler_rotation: Vector3d):
        pass
