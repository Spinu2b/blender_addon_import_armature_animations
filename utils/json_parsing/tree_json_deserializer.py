from typing import Tuple, Any, List

from ...utils.model.tree_hierarchy import TreeNodeContainer
from ...utils.json_parsing.json_parsing_helper import JsonParsingHelper
from ...utils.json_parsing.json_deserializer import JsonDeserializer


class TreeNodeChildrenListJsonDeserializer:
    @classmethod
    def deserialize(cls, json_string: str, parsing_start_char_index: int, tree_node_json_deserializer_class: Any,
                    tree_node_key_json_deserializer_class: Any) -> Tuple[List[TreeNodeContainer], int]:
        result = []  # type: List[TreeNodeContainer]

        parsing_start_char_index = JsonParsingHelper.go_to_next_value_in_json_list(
            json_string, parsing_start_char_index
        )
        old_parsing_start_char_index = JsonParsingHelper.INVALID_CHAR_INDEX
        while parsing_start_char_index != JsonParsingHelper.INVALID_CHAR_INDEX:
            current_node, parsing_start_char_index = TreeNodeContainerJsonDeserializer.deserialize(
                json_string=json_string, parsing_start_char_index=parsing_start_char_index,
                tree_node_json_deserializer_class=tree_node_json_deserializer_class,
                tree_node_key_json_deserializer_class=tree_node_key_json_deserializer_class
            )
            result.append(current_node)
            old_parsing_start_char_index = parsing_start_char_index
            attribute_name, parsing_start_char_index = JsonParsingHelper.go_to_next_value_in_json_list(
                json_string, parsing_start_char_index)

        return result, old_parsing_start_char_index


class TreeNodeContainerJsonDeserializer:
    CHILDREN_ATTRIBUTE_LABEL = None
    NODE_ATTRIBUTE_LABEL = None
    KEY_ATTRIBUTE_LABEL = None

    @classmethod
    def deserialize(cls, json_string: str, parsing_start_char_index: int,
                    tree_node_json_deserializer_class: Any, tree_node_key_json_deserializer_class: Any) ->\
            Tuple[TreeNodeContainer, int]:
        result = TreeNodeContainer(key=None, node=None)
        attribute_name, parsing_start_char_index = JsonParsingHelper.get_next_attribute_in_json_object(
            json_string, parsing_start_char_index)
        old_parsing_start_char_index = -1
        while parsing_start_char_index != JsonParsingHelper.INVALID_ATTRIBUTE_CODE:
            if attribute_name == cls.KEY_ATTRIBUTE_LABEL:
                key_value, parsing_start_char_index = tree_node_key_json_deserializer_class.deserialize(
                    json_string=json_string,
                    parsing_start_char_index=parsing_start_char_index
                )
                result.key = key_value
            elif attribute_name == cls.NODE_ATTRIBUTE_LABEL:
                node_object, parsing_start_char_index = tree_node_json_deserializer_class.deserialize(
                    json_string=json_string,
                    parsing_start_char_index=parsing_start_char_index
                )
                result.node = node_object
            elif attribute_name == cls.CHILDREN_ATTRIBUTE_LABEL:
                node_children_list, parsing_start_char_index = \
                    TreeNodeChildrenListJsonDeserializer.deserialize(
                        json_string=json_string,
                        parsing_start_char_index=parsing_start_char_index,
                        tree_node_json_deserializer_class=tree_node_json_deserializer_class,
                        tree_node_key_json_deserializer_class=tree_node_key_json_deserializer_class
                    )
                result.children = node_children_list
            else:
                raise ValueError('Something went wrong during JSON tree node deserialization!')

            old_parsing_start_char_index = parsing_start_char_index
            attribute_name, parsing_start_char_index = JsonParsingHelper.get_next_attribute_in_json_object(
                json_string, parsing_start_char_index)
        return result, old_parsing_start_char_index


class TreeJsonDeserializer(JsonDeserializer):
    TREE_NODE_KEY_JSON_DESERIALIZER_CLASS = None
    TREE_NODE_JSON_DESERIALIZER_CLASS = None
    RESULT_CLASS = None

    ROOT_ATTRIBUTE_LABEL = "Root"

    @classmethod
    def deserialize(cls, json_string: str, parsing_start_char_index: int = 0) -> Tuple[Any, int]:
        result = cls.RESULT_CLASS()
        attribute_name, parsing_start_char_index = JsonParsingHelper.get_next_attribute_in_json_object(
            json_string, parsing_start_char_index)
        while parsing_start_char_index != JsonParsingHelper.INVALID_ATTRIBUTE_CODE:
            if attribute_name == cls.ROOT_ATTRIBUTE_LABEL:
                root_node, parsing_start_char_index = TreeNodeContainerJsonDeserializer.deserialize(
                    json_string=json_string,
                    parsing_start_char_index=parsing_start_char_index,
                    tree_node_json_deserializer_class=cls.TREE_NODE_JSON_DESERIALIZER_CLASS,
                    tree_node_key_json_deserializer_class=cls.TREE_NODE_KEY_JSON_DESERIALIZER_CLASS
                )
                result.root = root_node
                return result, parsing_start_char_index
            else:
                raise ValueError('Encountered another attribute name than root during JSON tree deserialization!')

        raise ValueError('Invalid body of JSON tree for deserialization!')
