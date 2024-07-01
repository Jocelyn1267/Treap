""" Node Class (basic data structure of the Treap class)"""

from typing import Union

class Node:
    # member variables
    key: str
    priority: Union[int, None]
    parent: Union["Node", None] = None
    left: Union["Node", None] = None
    right: Union["Node", None] = None

    def __init__(self,
                 key: str,
                 priority: Union[int, None] = None) -> None:

        self.key = key
        self.priority = priority

    def __str__(self):
        # representation is key (priority)
        return "{} ({})".format(self.key, self.priority)

