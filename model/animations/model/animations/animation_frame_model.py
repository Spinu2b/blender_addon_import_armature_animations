import copy

from .....utils.model_spaces_integration.model_spaces_info import ModelSpacesInfo
from .....model.objects.model.export_objects_library_model_description.armature_bind_pose_model import\
    ArmatureBindPoseModel
from .....model.animations.model.blender_pose_mode_animation_frame_model import BlenderPoseModeAnimationFrameModel, \
    BlenderPoseModeAnimationFrameModelNode
from .....utils.model_spaces_integration.axis_info import AxisInfo
from .....utils.model_spaces_integration.model_quaternion import ModelQuaternion
from .....utils.model_spaces_integration.model_vector3d import ModelVector3d
from .....utils.model_spaces_integration.quaternion import Quaternion
from .....utils.model_spaces_integration.vector3d import Vector3d
from .....utils.model.tree_hierarchy import TreeHierarchy


class AnimationFrameNodeModel:
    def __init__(self,
                 node_name : str = "",
                 position: Vector3d = Vector3d(),
                 local_position: Vector3d = Vector3d(),
                 rotation: Quaternion = Quaternion(),
                 local_rotation: Quaternion = Quaternion(),
                 scale: Vector3d = Vector3d(),
                 local_scale: Vector3d = Vector3d(),
                 has_bone: bool = True):
        self.node_name = node_name  # type: str
        self.position = copy.deepcopy(position)  # type: Vector3d
        self.local_position = copy.deepcopy(local_position)  # type: Vector3d
        self.rotation = copy.deepcopy(rotation)  # type: Quaternion
        self.local_rotation = copy.deepcopy(local_rotation)  # type: Quaternion
        self.scale = copy.deepcopy(scale)  # type: Vector3d
        self.local_scale = copy.deepcopy(local_scale)  # type: Vector3d
        self.has_bone = has_bone

    @classmethod
    def from_json_dict_tree_building(cls, json_dict):
        return AnimationFrameNodeModel(
            node_name=json_dict["boneName"],
            position=ModelVector3d(
                x=float(json_dict["position"]["x"]),
                y=float(json_dict["position"]["y"]),
                z=float(json_dict["position"]["z"]),
                axis_info=ModelSpacesInfo.MODEL_AXIS_INFO).\
            translate_to_model_axis(target_axis_info=ModelSpacesInfo.BLENDER_AXIS_INFO).to_vector3d(),
            local_position=ModelVector3d(
                x=float(json_dict["localPosition"]["x"]),
                y=float(json_dict["localPosition"]["y"]),
                z=float(json_dict["localPosition"]["z"]),
                axis_info=ModelSpacesInfo.MODEL_AXIS_INFO).\
            translate_to_model_axis(target_axis_info=ModelSpacesInfo.BLENDER_AXIS_INFO).to_vector3d(),
            rotation=ModelQuaternion(
                w=float(json_dict["rotation"]["w"]),
                x=float(json_dict["rotation"]["x"]),
                y=float(json_dict["rotation"]["y"]),
                z=float(json_dict["rotation"]["z"]),
                axis_info=ModelSpacesInfo.MODEL_AXIS_INFO
            ).translate_to_model_axis(target_axis_info=ModelSpacesInfo.BLENDER_AXIS_INFO).to_quaternion(),
            local_rotation=ModelQuaternion(
                w=float(json_dict["localRotation"]["w"]),
                x=float(json_dict["localRotation"]["x"]),
                y=float(json_dict["localRotation"]["y"]),
                z=float(json_dict["localRotation"]["z"]),
                axis_info=ModelSpacesInfo.MODEL_AXIS_INFO
            ).translate_to_model_axis(target_axis_info=ModelSpacesInfo.BLENDER_AXIS_INFO).to_quaternion(),
            scale=ModelVector3d(
                x=float(json_dict["scale"]["x"]),
                y=float(json_dict["scale"]["y"]),
                z=float(json_dict["scale"]["z"]),
                axis_info=ModelSpacesInfo.MODEL_AXIS_INFO).\
            translate_to_model_axis(target_axis_info=ModelSpacesInfo.BLENDER_AXIS_INFO).to_vector3d(),
            local_scale=ModelVector3d(
                x=float(json_dict["localScale"]["x"]),
                y=float(json_dict["localScale"]["y"]),
                z=float(json_dict["localScale"]["z"]),
                axis_info=ModelSpacesInfo.MODEL_AXIS_INFO).\
            translate_to_model_axis(target_axis_info=ModelSpacesInfo.BLENDER_AXIS_INFO).to_vector3d()
        )

    def translate_to_space_model(self, base_space_model: AxisInfo, target_space_model: AxisInfo):
        self.position = ModelVector3d(
            x=self.position.x, y=self.position.y, z=self.position.z,
            axis_info=base_space_model).translate_to_model_axis(target_axis_info=target_space_model).to_vector3d()
        self.local_position = ModelVector3d(
            x=self.local_position.x, y=self.local_position.y, z=self.local_position.z,
            axis_info=base_space_model).translate_to_model_axis(target_axis_info=target_space_model).to_vector3d()
        self.rotation = ModelQuaternion(
            w=self.rotation.w, x=self.rotation.x, y=self.rotation.y, z=self.rotation.z,
            axis_info=base_space_model
        ).translate_to_model_axis(target_axis_info=target_space_model).to_quaternion()
        self.local_rotation = ModelQuaternion(
            w=self.local_rotation.w, x=self.local_rotation.x, y=self.local_rotation.y, z=self.local_rotation.z,
            axis_info=base_space_model
        ).translate_to_model_axis(target_axis_info=target_space_model).to_quaternion()
        self.scale = ModelVector3d(
            x=self.scale.x, y=self.scale.y, z=self.scale.z,
            axis_info=base_space_model).translate_to_model_axis(target_axis_info=target_space_model).to_vector3d()
        self.local_scale = ModelVector3d(
            x=self.local_scale.x, y=self.local_scale.y, z=self.local_scale.z,
            axis_info=base_space_model).translate_to_model_axis(target_axis_info=target_space_model).to_vector3d()


class AnimationFrameModel(TreeHierarchy):
    def translate_to_space_model(self, base_space_model: AxisInfo, target_space_model: AxisInfo):
        for node_iter in self.iterate_nodes():
            node_iter.node.translate_to_space_model(
                base_space_model=base_space_model, target_space_model=target_space_model)

    def get_blender_pose_mode_animation_frame_model(
            self, armature_bind_pose_model: ArmatureBindPoseModel) -> BlenderPoseModeAnimationFrameModel:
        result = BlenderPoseModeAnimationFrameModel()
        animation_frame_nodes_iters_dict = {node_iter.key: node_iter for node_iter in self.iterate_nodes()}
        for bind_pose_model_node_iter in armature_bind_pose_model.iterate_nodes():
            if bind_pose_model_node_iter.key in animation_frame_nodes_iters_dict:
                result.add_node(
                    parent_key=animation_frame_nodes_iters_dict[bind_pose_model_node_iter.key].parent_key,
                    node_key=animation_frame_nodes_iters_dict[bind_pose_model_node_iter.key].key,
                    node=BlenderPoseModeAnimationFrameModelNode(
                        bone_name=animation_frame_nodes_iters_dict[bind_pose_model_node_iter.key].node.node_name,
                        position=animation_frame_nodes_iters_dict[bind_pose_model_node_iter.key].node.position,
                        rotation=animation_frame_nodes_iters_dict[bind_pose_model_node_iter.key].node.rotation,
                        scale=animation_frame_nodes_iters_dict[bind_pose_model_node_iter.key].node.scale
                    )
                )
            else:
                result.add_node(
                    parent_key=bind_pose_model_node_iter.parent_key,
                    node_key=bind_pose_model_node_iter.key,
                    node=BlenderPoseModeAnimationFrameModelNode(
                        bone_name=bind_pose_model_node_iter.node.name,
                        position=Vector3d(0.0, 0.0, 0.0),
                        rotation=Quaternion(1.0, 0.0, 0.0, 0.0),
                        scale=Vector3d(0.0001, 0.0001, 0.0001)
                    )
                )
        return result
