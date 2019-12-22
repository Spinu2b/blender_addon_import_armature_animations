from ....utils.model_spaces_integration.euler_rotation_model_vector3d import EulerRotationModelVector3d
from ....utils.model_spaces_integration.vector3d import Vector3d


class BlenderEditModeBone:
    def __init__(self, head_position: Vector3d, tail_position: Vector3d):
        self.head_position = head_position  # type: Vector3d
        self.tail_position = tail_position  # type: Vector3d

    def get_bone_center(self) -> Vector3d:
        return (self.head_position + self.tail_position) / 2.0

    def position_using_bone_center(self, center_position: Vector3d):
        # position is basis for later work with mesh
        # practically all the bones could just sit in one place in space in edit mode
        # but then for human being it would be pain in the ass to assign vertices groups to bones in such edit mode
        # so we must in this phase position bones in space and treat such arrangement as home position of armature
        # when later positioning bones in pose mode - keep that in mind, it is very important

        head_position_from_center_vector = self.head_position - self.get_bone_center()  # type: Vector3d
        tail_position_from_center_vector = self.tail_position - self.get_bone_center()  # type: Vector3d
        self.head_position = center_position + head_position_from_center_vector
        self.tail_position = center_position + tail_position_from_center_vector

    def scale_as_if_inside_bounding_box(self, absolute_scale: Vector3d):
        # Treat bone as if it was a diagonal of imaginary bounding box in order
        # to take into account all of three spatial scaling
        # factors - x, y and z

        # for now do nothing - just make all bones equal length, it shouldn't matter when assigning vertices groups
        # to bones
        # in theory the whole armature could be even smaller than the actual mesh it animates
        # yet still properly deforming it
        # all that matters are vertices sets that are assigned to each bone - its scope of affection.
        # when taking into account armature home position, relative bones' scales in pose mode should properly
        # map to all the animations clips and we are good to go anyway

        # that saves us some boring time of actually implementing it
        pass

    def rotate_using_euler_angles(self, absolute_euler_rotation: EulerRotationModelVector3d):
        # rotation could not necessarily be needed, yet it gives better picture of how the bones are
        # positioned and stuff
        # it provides more convenient view on the armature, and makes later working in Blender and life in general
        # easier

        head_position_from_center_vector = self.head_position - self.get_bone_center()  # type: Vector3d
        tail_position_from_center_vector = self.tail_position - self.get_bone_center()  # type: Vector3d

        in_forward_plane_rotation, in_up_plane_rotation, in_side_plane_rotation = absolute_euler_rotation.\
            get_in_plane_rotations()

        in_forward_plane_rotation_matrix = in_side_plane_rotation.get_rotation_matrix()
        in_up_plane_rotation_matrix = in_up_plane_rotation.get_rotation_matrix()
        in_side_plane_rotation_matrix = in_side_plane_rotation.get_rotation_matrix()

        head_position_from_center_vector = in_forward_plane_rotation_matrix.multiply_to_vector(
            head_position_from_center_vector)
        head_position_from_center_vector = in_up_plane_rotation_matrix.multiply_to_vector(
            head_position_from_center_vector
        )
        head_position_from_center_vector = in_side_plane_rotation_matrix.multiply_to_vector(
            head_position_from_center_vector
        )

        tail_position_from_center_vector = in_forward_plane_rotation_matrix.multiply_to_vector(
            tail_position_from_center_vector)
        tail_position_from_center_vector = in_up_plane_rotation_matrix.multiply_to_vector(
            tail_position_from_center_vector
        )
        tail_position_from_center_vector = in_side_plane_rotation_matrix.multiply_to_vector(
            tail_position_from_center_vector
        )

        self.head_position = self.get_bone_center() + head_position_from_center_vector
        self.tail_position = self.get_bone_center() + tail_position_from_center_vector
