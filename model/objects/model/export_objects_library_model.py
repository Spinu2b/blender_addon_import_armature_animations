import copy
from typing import Dict, Set, Tuple

from ....model.animations.model.animations.animation_frame_model import AnimationFrameModel
from ....model.animations.model.animations.animation_clip_model import AnimationClipModel
from ....model.animations.model.armature_with_animation_clips_model import ArmatureWithAnimationClipsModel
from ....model.objects.constructing.armature.armature_bind_pose_model_constructor import \
    ArmatureBindPoseModelConstructor
from ....model.objects.model.export_objects_library_model_description.armature_bind_pose_model import \
    ArmatureBindPoseModel
from ....model.objects.model.animated_export_object_model import AnimatedExportObjectModel
from ....utils.model_spaces_integration.axis_info import AxisInfo
from ....model.objects.model.export_objects_library_model_description.armature_hierarchy_model import \
    ArmatureHierarchyModel, ArmatureHierarchyModelNode


class AnimationFramesHierarchiesConsolidator:
    def consolidate(self, armature_hierarchy_model: ArmatureHierarchyModel, animation_frame: AnimationFrameModel):
        armature_parent_child_pairs_set = set(armature_hierarchy_model.iterate_parent_child_key_pairs())
        animation_frame_parent_child_pairs_set = \
            set(animation_frame.iterate_parent_child_key_pairs())

        # if not armature_parent_child_pairs_set.issubset(animation_frame_parent_child_pairs_set):
        #     raise ValueError("Improperly composed bones hierarchy among armature model and animation frame!")

        new_armature_parent_child_pairs_set = animation_frame_parent_child_pairs_set.difference(
            armature_parent_child_pairs_set)

        self._add_new_armature_hierarchy_nodes(
            armature_hierarchy_model=armature_hierarchy_model,
            new_nodes=new_armature_parent_child_pairs_set
        )

    def _add_new_armature_hierarchy_nodes(
            self, armature_hierarchy_model: ArmatureHierarchyModel, new_nodes: Set[Tuple[str, str]]):
        new_nodes = copy.deepcopy(new_nodes)
        new_nodes_infos = {(node_info[0], node_info[1],
                            ArmatureHierarchyModelNode(bone_name=node_info[1])) for node_info in new_nodes}

        armature_hierarchy_model.extend_tree_hierarchy(new_nodes_infos=new_nodes_infos)


class ExportObjectsLibraryModel:
    def __init__(self):
        self.armature_hierarchy = ArmatureHierarchyModel()
        self.animated_export_objects = dict()  # type: Dict[str, AnimatedExportObjectModel]

    def translate_to_space_model(
            self, base_space_model: AxisInfo, target_space_model: AxisInfo):
        for animated_export_object_name in self.animated_export_objects:
            self.animated_export_objects[animated_export_object_name].translate_to_space_model(
                base_space_model=base_space_model, target_space_model=target_space_model
            )

    def reform_for_blender_building_process(self):
        self._check_one_channel_to_one_mesh_assumption()

    # how far two meshes' bind poses of one channel may differ and still count as the same bind pose
    BIND_POSE_AGREEMENT_EPSILON = 1e-4

    def _check_one_channel_to_one_mesh_assumption(self):
        """Several meshes may be skinned to one channel (e.g. the submeshes of one R3 object, one per material: an
        opaque and an alpha one) as long as they agree on its bind pose: the armature has one bind pose per bone (the
        first mesh's, ArmatureBindPoseModelConstructor). Meshes that disagree cannot share the armature."""
        channel_bind_pose_owner_dict = dict()  # type: Dict[str, str]
        for channel_node_iter in self.armature_hierarchy.iterate_nodes():
            channel_name = channel_node_iter.node.bone_name
            for anim_export_object_name in self.animated_export_objects:
                anim_export_object = self.animated_export_objects[anim_export_object_name]
                if channel_name not in anim_export_object.bind_bone_poses:
                    continue
                if channel_name not in channel_bind_pose_owner_dict:
                    channel_bind_pose_owner_dict[channel_name] = anim_export_object_name
                    continue
                owner_name = channel_bind_pose_owner_dict[channel_name]
                if not self._bind_poses_agree(
                        self.animated_export_objects[owner_name].bind_bone_poses[channel_name],
                        anim_export_object.bind_bone_poses[channel_name]):
                    raise ValueError(
                        "Meshes {} and {} disagree on the bind pose of {}: they cannot share one armature".format(
                            owner_name, anim_export_object_name, channel_name))

    def _bind_poses_agree(self, first, second) -> bool:
        first_values = (first.position.x, first.position.y, first.position.z,
                        first.scale.x, first.scale.y, first.scale.z)
        second_values = (second.position.x, second.position.y, second.position.z,
                         second.scale.x, second.scale.y, second.scale.z)
        if any(abs(a - b) > self.BIND_POSE_AGREEMENT_EPSILON for a, b in zip(first_values, second_values)):
            return False
        # q and -q are the same rotation
        quaternions_dot = first.rotation.w * second.rotation.w + first.rotation.x * second.rotation.x + \
            first.rotation.y * second.rotation.y + first.rotation.z * second.rotation.z
        return abs(abs(quaternions_dot) - 1.0) <= self.BIND_POSE_AGREEMENT_EPSILON

    def get_armature_bind_pose_model(self) -> ArmatureBindPoseModel:
        armature_bind_pose_model_constructor = ArmatureBindPoseModelConstructor()
        return armature_bind_pose_model_constructor.construct(self.armature_hierarchy, self.animated_export_objects)

    def comprehend_animations_armature_hierarchies(
            self, armature_animation_clips_model: ArmatureWithAnimationClipsModel):
        animation_frames_hierarchies_consolidator = AnimationFramesHierarchiesConsolidator()
        for animation_clip_name in armature_animation_clips_model.get_animation_clips():
            animation_clip = armature_animation_clips_model. \
                get_animation_clips()[animation_clip_name]  # type: AnimationClipModel
            first_animation_frame = animation_clip.get_first_animation_frame()  # type: AnimationFrameModel
            animation_frames_hierarchies_consolidator.consolidate(
                armature_hierarchy_model=self.armature_hierarchy,
                animation_frame=first_animation_frame
            )
