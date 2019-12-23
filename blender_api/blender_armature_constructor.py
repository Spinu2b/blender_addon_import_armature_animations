from typing import TYPE_CHECKING
from ..blender_api.blender_operations.constructing_armature.blender_armature_generator import BlenderArmatureGenerator

if TYPE_CHECKING:
    from bpy.types import Armature
    from ..animations_model.model.armature.blender.blender_edit_mode_armature_model import BlenderEditModeArmatureModel


class BlenderArmatureConstructor:
    def build_armature(self,
                       name: str,
                       blender_edit_mode_armature_model: 'BlenderEditModeArmatureModel') -> 'Armature':
        blender_armature_generator = BlenderArmatureGenerator()
        armature = blender_armature_generator.create_armature(name=name)  # type: Armature
        for armature_bone_model in blender_edit_mode_armature_model.iterate_nodes():
            blender_armature_generator.place_bone(
                armature_bone_model=armature_bone_model.node,
                armature=armature)

        for child_parent_pair in blender_edit_mode_armature_model.iterate_all_child_parent_pairs():
            blender_armature_generator.parent_bone_to(
                child=child_parent_pair.child,
                parent=child_parent_pair.parent,
                armature=armature)

        return armature
