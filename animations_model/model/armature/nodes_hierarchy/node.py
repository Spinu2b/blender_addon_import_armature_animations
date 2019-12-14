from typing import List


class Node:
    def __init__(self, name: str):
        self.children = []  # type: List[Node]
        self.name = name  # type: str
