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
        new_nodes_infos = [(node_info[0], node_info[1],
                            ArmatureHierarchyModelNode(bone_name=node_info[1])) for node_info in new_nodes]

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

    def _check_one_channel_to_one_mesh_assumption(self):
        channel_meshes_count_dict = dict()  # type: Dict[str, int]
        for channel_node_iter in self.armature_hierarchy.iterate_nodes():
            channel_name = channel_node_iter.node.bone_name
            channel_meshes_count_dict[channel_name] = 0
            for anim_export_object_name in self.animated_export_objects:
                anim_export_object = self.animated_export_objects[anim_export_object_name]
                if channel_name in anim_export_object.bind_bone_poses or \
                        channel_name in anim_export_object.mesh_geometry.bones_weights:
                    channel_meshes_count_dict[channel_name] += 1
        for channel_name in channel_meshes_count_dict:
            if channel_meshes_count_dict[channel_name] > 1:
                raise ValueError("One channel to one mesh assumption is not satisfied!")

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
