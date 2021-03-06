from typing import Tuple
from bpy.types import Armature, Object

from ..model.animations.model.blender_edit_mode_armature_model import BlenderEditModeArmatureModel
from ..blender_api.blender_operations.constructing_armature.blender_armature_generator import BlenderArmatureGenerator


class BlenderArmatureConstructor:
    def build_armature(self,
                       name: str,
                       blender_edit_mode_armature_model: 'BlenderEditModeArmatureModel') -> Tuple[Armature, Object]:
        blender_armature_generator = BlenderArmatureGenerator()
        armature, armature_obj = blender_armature_generator.create_armature(name=name)
        for armature_bone_model in blender_edit_mode_armature_model.iterate_nodes():
            blender_armature_generator.place_bone(
                armature_bone_model=armature_bone_model.node,
                armature=armature,
                armature_obj=armature_obj)

        for child_parent_pair in blender_edit_mode_armature_model.iterate_all_child_parent_pairs():
            if child_parent_pair.parent is not None:
                blender_armature_generator.parent_bone_to(
                    child=child_parent_pair.child,
                    #parent=child_parent_pair.parent,
                    parent=blender_edit_mode_armature_model.root.node,
                    armature=armature)

        return armature, armature_obj
