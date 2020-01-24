from typing import Dict

from bpy.types import Object


class BlenderRiggingHelper:
    def parent_blender_object_to_armature_with_bones_vertex_groups(
            self,
            armature_obj: Object,
            bones_vertex_groups: Dict[str, Dict[int, float]],
            blender_mesh_obj: Object):
        raise NotImplementedError
