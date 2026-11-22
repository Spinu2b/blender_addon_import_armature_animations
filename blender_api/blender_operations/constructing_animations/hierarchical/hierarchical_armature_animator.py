"""Exact import of Raymap animations into a hierarchical armature.

The flat importer poses every bone in world space from a location / rotation / scale, which cannot represent the
shear R3's non-uniform (squash & stretch) scales create in child channels. Here instead:

* the armature gets a parent hierarchy, every bone inheriting its parent's full matrix (inherit_scale 'FULL'),
  so a child of a non-uniformly scaled bone is sheared the same way Raymap / Unity shears it;
* R3 sets a channel's parent per frame and it changes between states, so for every bone the planner picks the parent
  that keeps the bone exactly representable in the most frames;
* where a bone still needs shear relative to its chosen parent (its frame parent differs and squashes), a helper
  bone "<bone>_shear" is inserted above it: the helper carries translation + rotation U + scale Sigma and the bone a
  rotation Vt (singular value decomposition), which composes to any affine matrix;
* keys are computed from Raymap's matrices directly (no pose evaluation), one key per R3 frame, linear.

Unity composes transforms the same way (parent @ T @ R @ S), so the FBX of this armature plays back exactly in Unity.
"""
import collections

import bpy
import numpy as np
from mathutils import Matrix

from .raymap_affine_math import (
    frame_unity_world_and_local_matrices_and_parents, unity_world_to_blender_armature_pose,
    unity_local_to_blender_bone_basis, columns_orthogonality_residual, decompose_trs, compose_trs, aligned_svd,
    COLUMNS_ORTHOGONALITY_EPSILON, HIDDEN_BONE_SCALE)

ROOT_BONE_NAME = "ROOT_CHANNEL"
SHEAR_HELPER_SUFFIX = "_shear"


class HierarchyPlan:
    def __init__(self):
        self.parent_of = {}  # bone -> chosen parent bone
        self.bones_with_shear_helper = set()
        self.report_lines = []

    def order_parents_first(self):
        ordered, placed = [], {ROOT_BONE_NAME}
        remaining = dict(self.parent_of)
        while remaining:
            ready = [bone for bone, parent in remaining.items() if parent in placed]
            if not ready:
                raise ValueError("Cycle in the planned hierarchy: {}".format(remaining))
            for bone in sorted(ready):
                ordered.append(bone)
                placed.add(bone)
                del remaining[bone]
        return ordered


class HierarchyPlanner:
    """Chooses, per bone, the parent with which the bone needs no shear in the most frames."""

    def plan(self, armature_bone_names, clips_frames_matrices) -> HierarchyPlan:
        bones = [b for b in armature_bone_names if b != ROOT_BONE_NAME]
        bone_set = set(bones)
        candidates = collections.defaultdict(collections.Counter)
        for frames in clips_frames_matrices.values():
            for matrices in frames.values():
                for bone in bones:
                    if bone in matrices:
                        frame_parent = matrices[bone][2]
                        candidate = frame_parent if frame_parent in bone_set else ROOT_BONE_NAME
                        candidates[bone][candidate] += 1

        scores = {}
        for bone in bones:
            options = set(candidates[bone]) | {ROOT_BONE_NAME}
            scored = []
            for candidate in options:
                parent_absent = sheared = 0
                worst = 0.0
                for frames in clips_frames_matrices.values():
                    for matrices in frames.values():
                        if bone not in matrices:
                            continue
                        if candidate == ROOT_BONE_NAME:
                            parent_world = np.eye(4)
                        elif candidate in matrices:
                            parent_world = matrices[candidate][0]
                        else:
                            parent_absent += 1
                            continue
                        relative = np.linalg.solve(parent_world, matrices[bone][0])
                        residual = columns_orthogonality_residual(relative[:3, :3])
                        if residual > COLUMNS_ORTHOGONALITY_EPSILON:
                            sheared += 1
                            worst = max(worst, residual)
                # prefer: parent present, no shear, most common frame parent
                scored.append(((parent_absent, sheared, worst, -candidates[bone][candidate]), candidate))
            scores[bone] = sorted(scored)

        plan = HierarchyPlan()
        frames_present = {bone: sum(candidates[bone].values()) for bone in bones}
        for bone in sorted(bones, key=lambda b: -frames_present[b]):
            for score, candidate in scores[bone]:
                if not self._creates_cycle(plan.parent_of, bone, candidate):
                    plan.parent_of[bone] = candidate
                    if score[1] > 0 or score[0] > 0:
                        plan.bones_with_shear_helper.add(bone)
                    plan.report_lines.append(
                        "{}: parent {} (frames with parent absent {}, sheared {}, worst residual {:.4f}){}".format(
                            bone, candidate, score[0], score[1], score[2],
                            " + shear helper" if bone in plan.bones_with_shear_helper else ""))
                    break
        return plan

    @staticmethod
    def _creates_cycle(parent_of, bone, candidate):
        current = candidate
        while current is not None and current != ROOT_BONE_NAME:
            if current == bone:
                return True
            current = parent_of.get(current)
        return False


class HierarchicalArmatureAnimator:
    def __init__(self):
        self.report_lines = []

    def restructure_and_animate(self, armature_obj, animation_clips_json: dict):
        # armature.bones is only up to date outside edit mode (the rig construction leaves it in edit mode)
        bpy.context.view_layer.objects.active = armature_obj
        if armature_obj.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        clips_frames_matrices = {
            clip_name: {int(frame): frame_unity_world_and_local_matrices_and_parents(frame_json)
                        for frame, frame_json in frames.items()}
            for clip_name, frames in animation_clips_json.items()}

        bone_names = [bone.name for bone in armature_obj.data.bones]
        plan = HierarchyPlanner().plan(bone_names, clips_frames_matrices)
        self.report_lines += plan.report_lines
        self._restructure_armature(armature_obj, plan)

        rest = {bone.name: np.array(bone.matrix_local) for bone in armature_obj.data.bones}
        ordered = plan.order_parents_first()
        for clip_name in sorted(clips_frames_matrices, key=self._clip_sort_key):
            self._animate_clip(armature_obj, clip_name, clips_frames_matrices[clip_name], plan, ordered, rest)

    @staticmethod
    def _clip_sort_key(name):
        tail = name.rsplit(' ', 1)[-1]
        return (0, int(tail)) if tail.isdigit() else (1, name)

    def _restructure_armature(self, armature_obj, plan: HierarchyPlan):
        bpy.context.view_layer.objects.active = armature_obj
        if armature_obj.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = armature_obj.data.edit_bones
        for bone in plan.bones_with_shear_helper:
            source = edit_bones[bone]
            helper = edit_bones.new(bone + SHEAR_HELPER_SUFFIX)
            helper.head, helper.tail, helper.roll = source.head.copy(), source.tail.copy(), source.roll
            helper.use_deform = False
        for bone, parent in plan.parent_of.items():
            edit_bone = edit_bones[bone]
            if bone in plan.bones_with_shear_helper:
                helper = edit_bones[bone + SHEAR_HELPER_SUFFIX]
                helper.use_connect = False
                helper.parent = edit_bones[parent]
                edit_bone.use_connect = False
                edit_bone.parent = helper
            else:
                edit_bone.use_connect = False
                edit_bone.parent = edit_bones[parent]
        for edit_bone in edit_bones:
            edit_bone.inherit_scale = 'FULL'
            edit_bone.use_inherit_rotation = True
            edit_bone.use_local_location = True
        bpy.ops.object.mode_set(mode='OBJECT')
        for pose_bone in armature_obj.pose.bones:
            pose_bone.rotation_mode = 'QUATERNION'

    def _animate_clip(self, armature_obj, clip_name, frames_matrices, plan, ordered, rest):
        frame_numbers = sorted(frames_matrices)
        # per animated bone: list of (location, quaternion wxyz, scale) per frame
        tracks = collections.defaultdict(list)
        svd_state = {}
        for frame_number in frame_numbers:
            matrices = frames_matrices[frame_number]
            pose = {ROOT_BONE_NAME: rest[ROOT_BONE_NAME]}
            tracks[ROOT_BONE_NAME].append(self._trs_key(np.eye(4)))
            for bone in ordered:
                parent = plan.parent_of[bone]
                helper = bone + SHEAR_HELPER_SUFFIX if bone in plan.bones_with_shear_helper else None
                # pose(child) = pose(parent) @ rest(parent)^-1 @ rest(child) @ basis(child)   (inherit_scale FULL)
                to_bone_rest = np.linalg.solve(rest[bone], rest[parent])
                if bone not in matrices:
                    helper_basis = np.eye(4)
                    bone_basis = np.diag([HIDDEN_BONE_SCALE, HIDDEN_BONE_SCALE, HIDDEN_BONE_SCALE, 1.0])
                else:
                    world, local, _ = matrices[bone]
                    wanted = unity_world_to_blender_armature_pose(world)
                    needed = to_bone_rest @ np.linalg.solve(pose[parent], wanted)
                    if helper is None:
                        bone_basis = compose_trs(*decompose_trs(needed))
                        helper_basis = None
                    else:
                        local_basis = unity_local_to_blender_bone_basis(local)
                        correction = needed @ np.linalg.inv(local_basis)
                        if columns_orthogonality_residual(correction[:3, :3]) <= COLUMNS_ORTHOGONALITY_EPSILON:
                            helper_basis = compose_trs(*decompose_trs(correction))
                            bone_basis = compose_trs(*decompose_trs(local_basis))
                            t, r, s = decompose_trs(correction)
                            svd_state[bone] = (r, np.eye(3))
                        else:
                            previous_u, previous_vt = svd_state.get(bone, (None, None))
                            u, sigma, vt = aligned_svd(correction[:3, :3], previous_u, previous_vt)
                            svd_state[bone] = (u, vt)
                            helper_basis = compose_trs(correction[:3, 3], u, sigma)
                            rotate_vt = np.eye(4)
                            rotate_vt[:3, :3] = vt
                            bone_basis = compose_trs(*decompose_trs(rotate_vt @ local_basis))
                if helper is None:
                    pose[bone] = pose[parent] @ np.linalg.inv(to_bone_rest) @ bone_basis
                else:
                    helper_pose = pose[parent] @ np.linalg.inv(to_bone_rest) @ helper_basis
                    pose[helper] = helper_pose
                    pose[bone] = helper_pose @ bone_basis  # helper rest == bone rest
                    tracks[helper].append(self._trs_key(helper_basis))
                tracks[bone].append(self._trs_key(bone_basis))

        action = bpy.data.actions.new(name=clip_name)
        action.use_fake_user = True
        if armature_obj.animation_data is None:
            armature_obj.animation_data_create()
        armature_obj.animation_data.action = action
        blender_frames = [frame_number + 1 for frame_number in frame_numbers]
        if len(blender_frames) == 1:
            # a one-frame action is exported to FBX without curves (Unity then gets an empty clip): hold the pose
            # for one more frame
            blender_frames.append(blender_frames[0] + 1)
            for bone_name in tracks:
                tracks[bone_name].append(tracks[bone_name][0])
        for bone_name, keys in tracks.items():
            self._write_track(action, armature_obj, bone_name, blender_frames, keys)

    @staticmethod
    def _trs_key(basis):
        translation, rotation, scale = decompose_trs(basis)
        quaternion = Matrix(rotation.tolist()).to_quaternion()
        return tuple(translation), (quaternion.w, quaternion.x, quaternion.y, quaternion.z), tuple(scale)

    def _write_track(self, action, armature_obj, bone_name, blender_frames, keys):
        # keep consecutive quaternions in the same hemisphere so linear interpolation takes the short way
        quaternions = [list(k[1]) for k in keys]
        for i in range(1, len(quaternions)):
            if np.dot(quaternions[i], quaternions[i - 1]) < 0:
                quaternions[i] = [-c for c in quaternions[i]]
        channels = (("location", [k[0] for k in keys]), ("rotation_quaternion", quaternions),
                    ("scale", [k[2] for k in keys]))
        for prop, values in channels:
            data_path = 'pose.bones["{}"].{}'.format(bone_name, prop)
            for index in range(len(values[0])):
                fcurve = self._ensure_fcurve(action, armature_obj, data_path, index, bone_name)
                fcurve.keyframe_points.add(len(blender_frames))
                coordinates = []
                for frame, value in zip(blender_frames, values):
                    coordinates += [frame, value[index]]
                fcurve.keyframe_points.foreach_set("co", coordinates)
                fcurve.keyframe_points.foreach_set("interpolation", [1] * len(blender_frames))  # LINEAR
                fcurve.update()

    @staticmethod
    def _ensure_fcurve(action, armature_obj, data_path, index, group_name):
        if hasattr(action, "fcurve_ensure_for_datablock"):  # Blender 4.4+ (slotted actions)
            return action.fcurve_ensure_for_datablock(armature_obj, data_path, index=index, group_name=group_name)
        fcurve = action.fcurves.find(data_path, index=index)
        if fcurve is None:
            fcurve = action.fcurves.new(data_path, index=index, action_group=group_name)
        return fcurve
