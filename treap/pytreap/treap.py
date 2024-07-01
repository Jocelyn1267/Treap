""" Treap Class"""

import random
from typing import Union

from .node import Node

class Treap:


    def __init__(self) -> None:
        # default instantiation creates an empty treap
        self.root = None
        self._nodes = []

    def insert(self, key: str, priority: Union[int, None] = None) -> None:
        """ Insert a new key (and optionally a priority).

        Args:
            key: The string key of the new node.
            priority: An optional integer value; if None this is randomly generated.
        """
        # make sure this key hasn't been used previously
        if self.search(key):
            raise AssertionError("Key {} already in use.".format(key))

        # make sure the given priority is good or generate our own    
        if priority is not None and priority < 0:
            raise AssertionError("Priority must be greater than zero.")
        elif priority is None:
            priority = random.randint(0, 1000)
   
        # construct node object and insert
        node = Node(key, priority)
        self._insert(node)

        # save this node
        if self.root is None:
            self.root = node
        self._nodes.append(node)

    def _insert(self, node):
        # Internal method to perform an insert function while maintaining treap properties
        # This operation is accomplished in two steps:
        # 1) Perform normalal binary tree insert
        # 2) Reorder tree to ensure key priorities are descending

        # first, find an empty leaf and insert
        current = self.root
        while current is not None:
            if node.key > current.key:
                if not current.right:
                    # insert as the right leaf here
                    current.right = node
                    node.parent = current
                    break
                else:
                    current = current.right
            else:
                if not current.left:
                    # insert as the left node here
                    current.left = node
                    node.parent = current
                    break
                else:
                    current = current.left

        # next we need to re-prioritize the tree
        #  this entails walking back up the tree and rotating nodes that 
        #  have misplace priorities

        # convenience function to rotate out nodes
        #  assumes both x and x.right
        def _left_rotate(x):
            y = x.right
            x.right = y.left
            if y.left:
                y.left.parent = x
            y.parent = x.parent
            if not x.parent:
                # this is our new root
                self.root = y
            elif x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
            y.left = x
            x.parent = y
            return y

        def _right_rotate(y):
            x = y.left
            y.left = x.right
            if x.right:
                x.right.parent = y
            x.parent = y.parent
            if not y.parent:
                # this is our new root
                self.root = x
            elif y == y.parent.right:
                y.parent.right = x
            else:
                y.parent.left = x
            x.right = y
            y.parent = x
            return x

        # actually perform the re-prioritization
        current = node
        while current.parent is not None:
            # check if there's a priority mismatch
            if current.parent.priority < current.priority:
                # check if this should be a left- or right- rotation
                if current.parent.right == current:
                    current = _left_rotate(current.parent)
                else:
                    current = _right_rotate(current.parent)
            else:
                break

    def search(self, key: str) -> bool:
        """ Search for the given key in the treap and return True if found.

        Args:
            key: The string key to search for.

        Returns:
            Boolean indicating success or failure.
        """

        # traverse tree looking for a matching key
        found = False
        current = self.root
        while current is not None:
            # check if this node matches our key and/or which child tree to check
            if current.key == key:
                found = True
                break
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        # return result
        return found

    def display(self):
        """ Print out the current treap"""
        def _display(node, level):
            if node is not None:
                _display(node.right, level+1)
                print("\t" * level + "-> {}".format(node))
                _display(node.left, level+1)

        # print("#"*80)
        print("Treap: ")
        _display(self.root, 0)
        print("#"*100)

    def __len__(self) -> int:
        # return the current size of the treap
        return len(self._nodes)

    def __iter__(self):
        return iter(self._nodes)
