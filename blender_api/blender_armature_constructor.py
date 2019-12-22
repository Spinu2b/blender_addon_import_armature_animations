from animations_model.model.armature.blender.blender_edit_mode_armature_model import BlenderEditModeArmatureModel
from blender_api.blender_operations.constructing_armature.blender_armature_generator import BlenderArmatureGenerator


class BlenderArmatureConstructor:
    def build_armature(self, blender_edit_mode_armature_model: BlenderEditModeArmatureModel):
        blender_armature_generator = BlenderArmatureGenerator()
        blender_armature_generator.create_armature()
        for armature_bone_model in blender_edit_mode_armature_model.iterate_nodes():
            blender_armature_generator.place_bone(armature_bone_model.node)

        for child_parent_pair in blender_edit_mode_armature_model.iterate_all_child_parent_pairs():
            blender_armature_generator.parent_bone_to(child_parent_pair.child, child_parent_pair.parent)
