from typing import Optional, Generator

from animations_model.model.armature.blender.blender_edit_mode_armature_node_model import \
    BlenderEditModeArmatureNodeModel


class BlenderEditModeArmatureModel:
    def __init__(self):
        self.root = None  # type: Optional[BlenderEditModeArmatureNodeModel]

    def add_node(self, parent_name: str, node: BlenderEditModeArmatureNodeModel):
        pass

    def iterate_all_armature_bones(self):
        pass
