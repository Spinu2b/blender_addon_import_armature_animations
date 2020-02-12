from typing import Iterator, Tuple


class JsonParsingHelper:
    @classmethod
    def iterate_object_attributes(cls, json_string: str, parsing_start_char_index: int) -> Iterator[Tuple[str, int]]:
        raise NotImplementedError
