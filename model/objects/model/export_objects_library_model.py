from ....model.objects.model.export_objects_library_model_description.armature_hierarchy_model import\
    ArmatureHierarchyModel


class ExportObjectsLibraryModel:
    def __init__(self):
        self.armature_hierarchy = ArmatureHierarchyModel()
        self.animated_export_objects = dict()
