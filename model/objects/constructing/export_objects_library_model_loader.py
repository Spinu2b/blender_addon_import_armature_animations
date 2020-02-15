from model.objects.json_parsing.export_objects_library_model_json_deserializer import \
    ExportObjectsLibraryModelJsonDeserializer
from ....model.objects.model.export_objects_library_model import ExportObjectsLibraryModel


class ExportObjectsLibraryModelLoader:
    def load(cls, path_to_json_file: str) -> 'ExportObjectsLibraryModel':
        with open(path_to_json_file, 'r') as json_file:
            json_string = json_file.read()
        return ExportObjectsLibraryModelJsonDeserializer.deserialize(
            json_string=json_string,
            parsing_start_char_index=0,
            result_class=ExportObjectsLibraryModel
        )
