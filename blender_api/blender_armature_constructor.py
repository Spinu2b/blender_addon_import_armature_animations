from blender_api.blender_operations.constructing_armature.blender_armature_generator import BlenderArmatureGenerator


class BlenderArmatureConstructor:
    def build_armature(self, unified_armature_model):
        blender_armature_generator = BlenderArmatureGenerator()
        blender_armature = blender_armature_generator.create_armature()
        for armature_bone_model in unified_armature_model.iterate_all_armature_bones():
            blender_armature_generator.place_bone(blender_armature, armature_bone_model)
