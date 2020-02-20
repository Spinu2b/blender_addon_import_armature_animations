import json

import orjson as orjson

from ....model.objects.constructing.export_objects_library_model_constructor import ExportObjectsLibraryModelConstructor
from ....model.objects.model.export_objects_library_model import ExportObjectsLibraryModel


class ExportObjectsLibraryModelLoader:
    def load(cls, path_to_json_file: str) -> 'ExportObjectsLibraryModel':
        with open(path_to_json_file, 'r') as json_file:
            json_string = json_file.read()  # type: str
            return orjson.loads(json_string)
        #with open(path_to_json_file, 'r') as json_file:
        #    json_dict = json.loads(json_file.read())
        #return ExportObjectsLibraryModelConstructor().construct_from_json(json_dict)
