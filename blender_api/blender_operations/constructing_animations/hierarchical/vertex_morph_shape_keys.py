"""R3 vertex morphs as shape keys, animated per clip.

The Raymap export gives, per mesh, the offsets of the vertices each morph target moves (in the exported mesh's space
and vertex order) and, per frame, a blend weight per (source PO, target PO). Every target becomes a shape key of the
mesh. Its value is driven by a custom property of the armature object ("morph_PO16_PO10"), and that property is keyed
in every clip's action next to the bones: the FBX exporter switches actions on the armature only, and bakes the
shape key values it evaluates, so each clip carries its own morph weights (blend shape curves in Unity).
"""
import bpy
import numpy as np


def morph_property_name(source_key: str, target_key: str) -> str:
    return "morph_{}_{}".format(source_key, target_key)


class VertexMorphShapeKeysBuilder:
    def __init__(self):
        self.report_lines = []

    def build(self, armature_obj, library_json: dict):
        """Creates the shape keys and drivers. Returns [(property name, source key, target key)]."""
        properties = []
        for object_name, export_object in library_json.get("animatedExportObjects", {}).items():
            targets = export_object.get("morphTargets")
            source_index = export_object.get("morphSourceObjectIndex", -1)
            if not targets or source_index is None or source_index < 0:
                continue
            mesh_obj = self._find_mesh_object(armature_obj, object_name)
            library_vertices = np.array([[v["x"], v["y"], v["z"]] for v in export_object["meshGeometry"]["vertices"]])
            if mesh_obj is None or len(mesh_obj.data.vertices) != len(library_vertices):
                self.report_lines.append("morphs of {}: mesh not found or vertex count differs, skipped".format(object_name))
                continue
            linear = self._library_to_mesh_linear_map(mesh_obj, library_vertices)
            source_key = "PO{}".format(source_index)
            if mesh_obj.data.shape_keys is None:
                mesh_obj.shape_key_add(name="Basis", from_mix=False)
            basis = np.array([v.co[:] for v in mesh_obj.data.vertices])
            for target_key in sorted(targets):
                coordinates = basis.copy()
                for vertex_index, offset in targets[target_key].items():
                    coordinates[int(vertex_index)] += linear @ np.array([offset["x"], offset["y"], offset["z"]])
                key_block = mesh_obj.shape_key_add(name=target_key, from_mix=False)
                key_block.data.foreach_set("co", coordinates.ravel())
                key_block.slider_min = 0.0
                key_block.slider_max = 10.0
                prop = morph_property_name(source_key, target_key)
                self._add_driven_property(armature_obj, prop, key_block)
                properties.append((prop, source_key, target_key))
            self.report_lines.append("morphs of {}: {} shape keys ({})".format(
                object_name, len(targets), ", ".join(sorted(targets))))
        return properties

    @staticmethod
    def _find_mesh_object(armature_obj, object_name):
        for obj in bpy.data.objects:
            if obj.type == 'MESH' and obj.parent == armature_obj and \
                    (obj.name == object_name + "_OBJECT_OBJECT" or obj.name.startswith(object_name[:50])):
                return obj
        return None

    @staticmethod
    def _library_to_mesh_linear_map(mesh_obj, library_vertices):
        # the mesh was built from these vertices through the addon's axis conversion: fit it (affine least squares)
        # and use its linear part for the offsets
        mesh_vertices = np.array([v.co[:] for v in mesh_obj.data.vertices])
        homogeneous = np.hstack([library_vertices, np.ones((len(library_vertices), 1))])
        solution, *_ = np.linalg.lstsq(homogeneous, mesh_vertices, rcond=None)
        return solution[:3, :].T

    @staticmethod
    def _add_driven_property(armature_obj, prop, key_block):
        armature_obj[prop] = 0.0
        try:
            ui = armature_obj.id_properties_ui(prop)
            ui.update(min=0.0, max=10.0, soft_min=0.0, soft_max=1.0)
        except (AttributeError, TypeError):
            pass
        fcurve = key_block.driver_add("value")
        driver = fcurve.driver
        driver.type = 'AVERAGE'
        variable = driver.variables.new()
        variable.name = "weight"
        variable.type = 'SINGLE_PROP'
        variable.targets[0].id_type = 'OBJECT'
        variable.targets[0].id = armature_obj
        variable.targets[0].data_path = '["{}"]'.format(prop)
