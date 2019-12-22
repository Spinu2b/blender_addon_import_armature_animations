from typing import List, Dict
from typing import TYPE_CHECKING

from ....animations_model.constructing.deriving_unified_armature.armature_nodes_hierarchy_helper import \
    ArmatureNodesHierarchyHelper

if TYPE_CHECKING:
    from ....animations_model.model.animations.animation_clip_model import AnimationClipModel
    from ....animations_model.model.armature.nodes_hierarchy.nodes_hierarchy import NodesHierarchy
    from ....animations_model.model.armature.unified_armature_model import UnifiedArmatureModel


class UnifiedArmatureModelConstructor:
    def derive_unified_armature_model_from_animation_clips(
            self, animation_clips: Dict[str, 'AnimationClipModel']) -> 'UnifiedArmatureModel':
        nodes_hierarchies = []  # type: List[NodesHierarchy]
        armature_nodes_hierarchy_helper = ArmatureNodesHierarchyHelper()
        for animation_clip in animation_clips:
            nodes_hierarchy = armature_nodes_hierarchy_helper.derive_nodes_hierarchy_from_animation_clip(
                animation_clips[animation_clip])
            nodes_hierarchies.append(nodes_hierarchy)
        unified_armature_model = armature_nodes_hierarchy_helper.\
            derive_most_comprehensive_armature_model_from_nodes_hierarchies(nodes_hierarchies)
        return unified_armature_model
