from typing import Tuple, List

from .....utils.model.tree_hierarchy import TreeNodeInfo, TreeNodeIter
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


class HandyMemoryPool:
    ALLOCATED_VECTORS_3D = []  # type: List[Vector3d]
    ALLOCATED_QUATERNIONS = []  # type: List[Quaternion]

    USED_VECTORS3D = 0
    USED_QUATERNIONS = 0

    ALLOCATION_CHUNK = 30000

    @classmethod
    def reallocate_vectors3d(cls):
        cls.ALLOCATED_VECTORS_3D.extend([Vector3d() for x in range(cls.ALLOCATION_CHUNK)])

    @classmethod
    def reallocate_quaternions(cls):
        cls.ALLOCATED_QUATERNIONS.extend([Quaternion() for x in range(cls.ALLOCATION_CHUNK)])

    @classmethod
    def get_vector3d(cls, coords: Tuple[float, float, float]) -> Vector3d:
        if len(cls.ALLOCATED_VECTORS_3D) <= cls.USED_VECTORS3D:
            cls.reallocate_vectors3d()

        vector3d = cls.ALLOCATED_VECTORS_3D[cls.USED_VECTORS3D]
        cls.USED_VECTORS3D += 1

        vector3d.x = coords[0]
        vector3d.y = coords[1]
        vector3d.z = coords[2]

        return vector3d

    @classmethod
    def get_quaternion(cls, coords: Tuple[float, float, float, float]) -> Quaternion:
        if len(cls.ALLOCATED_QUATERNIONS) <= cls.USED_QUATERNIONS:
            cls.reallocate_quaternions()

        quaternion = cls.ALLOCATED_QUATERNIONS[cls.USED_QUATERNIONS]
        cls.USED_QUATERNIONS += 1

        quaternion.w = coords[0]
        quaternion.x = coords[1]
        quaternion.y = coords[2]
        quaternion.z = coords[3]

        return quaternion


class AnimationFrameNodeModel:
    def __init__(self, node_name : str,
                 is_keyframe: bool,
                 position: Vector3d,
                 local_position: Vector3d,
                 rotation: Quaternion,
                 local_rotation: Quaternion,
                 scale: Vector3d,
                 local_scale: Vector3d):
        self.node_name = node_name  # type: str
        self.is_keyframe = is_keyframe  # type: bool
        self.position = position  # type: Vector3d
        self.local_position = local_position  # type: Vector3d
        self.rotation = rotation  # type: Quaternion
        self.local_rotation = local_rotation  # type: Quaternion
        self.scale = scale  # type: Vector3d
        self.local_scale = local_scale  # type: Vector3d

    @classmethod
    def from_json_dict_tree_building(cls, json_dict):
        def _translate_to_blender_axes3d(axes: Tuple[float, float, float]) -> Tuple[float, float, float]:
            return -axes[0], -axes[2], axes[1]

        def _translate_to_blender_axes_quaternion(axes: Tuple[float, float, float, float])\
                -> Tuple[float, float, float, float]:
            return -axes[0], -axes[1], -axes[3], axes[2]

        return AnimationFrameNodeModel(
             node_name=json_dict["boneName"],
             is_keyframe=bool(json_dict["isKeyframe"]),
             position=HandyMemoryPool.get_vector3d(
                 coords=_translate_to_blender_axes3d((
                     float(json_dict["position"]["x"]),
                     float(json_dict["position"]["y"]),
                     float(json_dict["position"]["z"]))
                 ),
             ),
             local_position=HandyMemoryPool.get_vector3d(
                  coords=_translate_to_blender_axes3d((
                      float(json_dict["localPosition"]["x"]),
                      float(json_dict["localPosition"]["y"]),
                      float(json_dict["localPosition"]["z"]))
                  ),
             ),
             rotation=HandyMemoryPool.get_quaternion(
                 coords=_translate_to_blender_axes_quaternion((
                     float(json_dict["rotation"]["w"]),
                     float(json_dict["rotation"]["x"]),
                     float(json_dict["rotation"]["y"]),
                     float(json_dict["rotation"]["z"]))
                 ),
             ),
             local_rotation=HandyMemoryPool.get_quaternion(
                 coords=_translate_to_blender_axes_quaternion((
                     float(json_dict["localRotation"]["w"]),
                     float(json_dict["localRotation"]["x"]),
                     float(json_dict["localRotation"]["y"]),
                     float(json_dict["localRotation"]["z"]))
                 ),
             ),
             scale=HandyMemoryPool.get_vector3d(
                 coords=_translate_to_blender_axes3d((
                     float(json_dict["scale"]["x"]),
                     float(json_dict["scale"]["y"]),
                     float(json_dict["scale"]["z"]))
                 ),
             ),
             local_scale=HandyMemoryPool.get_vector3d(
                 coords=_translate_to_blender_axes3d((
                     float(json_dict["localScale"]["x"]),
                     float(json_dict["localScale"]["y"]),
                     float(json_dict["localScale"]["z"]))
                 ),
             ),
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


class AnimationFrameModelToBlenderPoseModeAnimationFrameModelConverter:
    def convert(
            self, armature_bind_pose_model: ArmatureBindPoseModel,
            animation_frame_model,
            should_be_whole_keyframed: bool) -> BlenderPoseModeAnimationFrameModel:
        result = BlenderPoseModeAnimationFrameModel()

        nodes_building_infos = set()
        chains_bottom_nodes_keys_for_bones_chains_keyframing = []  # type: List[str]

        animation_frame_nodes_iters_dict = {node_iter.key: node_iter for node_iter in
                                            animation_frame_model.iterate_nodes()}
        for bind_pose_model_node_iter in armature_bind_pose_model.iterate_nodes():
            if bind_pose_model_node_iter.key in animation_frame_nodes_iters_dict:
                parent_key = animation_frame_nodes_iters_dict[bind_pose_model_node_iter.key].parent_key
                node_key = animation_frame_nodes_iters_dict[bind_pose_model_node_iter.key].key
                node = BlenderPoseModeAnimationFrameModelNode(
                    bone_name=animation_frame_nodes_iters_dict[bind_pose_model_node_iter.key].node.node_name,
                    is_keyframe=animation_frame_nodes_iters_dict[bind_pose_model_node_iter.key].node.is_keyframe
                    if not should_be_whole_keyframed else True,
                    position=animation_frame_nodes_iters_dict[bind_pose_model_node_iter.key].node.position,
                    rotation=animation_frame_nodes_iters_dict[bind_pose_model_node_iter.key].node.rotation,
                    scale=animation_frame_nodes_iters_dict[bind_pose_model_node_iter.key].node.scale
                )

                if not should_be_whole_keyframed and \
                        animation_frame_nodes_iters_dict[bind_pose_model_node_iter.key].node.is_keyframe:
                    chains_bottom_nodes_keys_for_bones_chains_keyframing.append(bind_pose_model_node_iter.key)
            else:
                parent_key = bind_pose_model_node_iter.parent_key
                node_key = bind_pose_model_node_iter.key
                node = BlenderPoseModeAnimationFrameModelNode(
                    bone_name=bind_pose_model_node_iter.node.name,
                    is_keyframe=False if not should_be_whole_keyframed else True,
                    position=Vector3d(0.0, 0.0, 0.0),
                    rotation=Quaternion(1.0, 0.0, 0.0, 0.0),
                    scale=Vector3d(0.0001, 0.0001, 0.0001)
                )

            nodes_building_infos.add((parent_key, node_key, node))

        result.extend_tree_hierarchy(new_nodes_infos=nodes_building_infos)

        for node_key in chains_bottom_nodes_keys_for_bones_chains_keyframing:
            self._keyframe_bones_chain_to_root_from_here(
                bottom_node_key=node_key,
                pose_mode_animation_frame_tree=result
            )

        return result

    def _keyframe_bones_chain_to_root_from_here(
            self,
            bottom_node_key: str,
            pose_mode_animation_frame_tree: BlenderPoseModeAnimationFrameModel):

        def _keyframe_all_bones_in_subtree(key: str, tree: BlenderPoseModeAnimationFrameModel):


        for node_iter in pose_mode_animation_frame_tree.iterate_from_this_node_towards_root(node_key=bottom_node_key):
            node_iter.node.is_keyframe = True

        _keyframe_all_bones_in_subtree(bottom_node_key, pose_mode_animation_frame_tree)


class AnimationFrameModel(TreeHierarchy):
    def translate_to_space_model(self, base_space_model: AxisInfo, target_space_model: AxisInfo):
        for node_iter in self.iterate_nodes():
            node_iter.node.translate_to_space_model(
                base_space_model=base_space_model, target_space_model=target_space_model)

    def get_blender_pose_mode_animation_frame_model(
            self, armature_bind_pose_model: ArmatureBindPoseModel,
            should_be_whole_keyframed: bool) -> BlenderPoseModeAnimationFrameModel:
        converter = AnimationFrameModelToBlenderPoseModeAnimationFrameModelConverter()
        return converter.convert(
            armature_bind_pose_model=armature_bind_pose_model,
            animation_frame_model=self,
            should_be_whole_keyframed=should_be_whole_keyframed
        )
