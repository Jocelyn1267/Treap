import os
import random
import timeit
import string
from pkg_resources import resource_filename

# from pytreap.treap import Treap

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


""" Treap Class"""

import random
from typing import Union

# from .node import Node


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
                _display(node.right, level + 1)
                print("\t" * level + "-> {}".format(node))
                _display(node.left, level + 1)

        # print("#"*80)
        print("Treap: ")
        _display(self.root, 0)
        print("#" * 100)

    def __len__(self) -> int:
        # return the current size of the treap
        return len(self._nodes)

    def __iter__(self):
        return iter(self._nodes)


TIMED_COUNT=10


def is_ordered(treap):
    """Rules:
     - if v is a child of u, then v.priority <= u.priority
     - if v is a left child of u, then v.key < u.key
     - if v is a right child of u, then v.key > u.key
    """
    # iterate through all nodes in the heap
    for node in treap:
        # check parent (if not root)
        if node != treap.root and (node.priority > node.parent.priority):
            print("Node {} and parent ({}) have mismatched priorities.".format(node, node.parent))
            return False
        # check left and right. All are optional, technically
        if node.left and (node.key < node.left.key):
            print("Node {} and left child ({}) have mismatched keys.".format(node, node.left))
            return False
        if node.right and (node.key > node.right.key):
            print("Node {} and right child ({}) have mismatched keys.".format(node, node.right))
            return False
    return True

def read_and_search(treap, data):
    """ Search for each character in the given file (non-case-sensitive) in the given Treap.
    Repeats this operation 10 times and prints out the average time.
    """
    # define core search method
    def _search():
        for c in data:
            if not(treap.search(c)):
                raise RuntimeError("Treap couldn't find expected key: '{}'.".format(c))

    print("Treap took {:.3f} seconds (average of {} tests) to search for {} characters.\n".format(
        timeit.timeit(_search, number=TIMED_COUNT)/TIMED_COUNT,
        TIMED_COUNT,
        len(data)))

def main():
    # seed random priorities
    random.seed()

    # find test data
    # test_file = os.path.abspath(resource_filename('pytreap.data', 'FellowshipOfTheRing.txt'))
    test_file = os.path.abspath('FellowshipOfTheRing.txt')
    test_data = open(test_file).read()
    test_data_cleaned = [c.upper() for c in test_data if c in string.ascii_letters]

    # define keys
    keys = ('Z','Y','X','W','V','B','U','G','M','R','K','J','D','Q',
            'E','C','S','I','H','P','L','A','N','O','T','F')


    ## Step 3

    print("Step 3")

    # construct the desired treap (priorities are generated randomly implicitly)
    uniform_treap = Treap()

    # add all the keys
    for key in keys:
        uniform_treap.insert(key)

    # print out the resulting treap
    uniform_treap.display()

    # check that this satisfies our conditions
    if is_ordered(uniform_treap):
        print("\nSUCCESS: Resulting treap satisfies our conditions.\n")
    else:
        print("\nERROR: Resulting treap is not ordered properly. Something went wrong.\n")
    
    ## Step 4

    print("Step 4")
    # test our speed against the Treap created in step #3
    read_and_search(uniform_treap, test_data_cleaned)

    ## Step 5

    print("Step 5")
    # construct and add keys and priorities to this new Treap
    heuristic_keys = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
    priorities = (24,7,14,17,26,10,8,18,22,4,5,16,13,19,23,12,2,20,21,25,15,6,11,3,9,1)
    heuristic_key_map = {k:p for k,p in zip(heuristic_keys, priorities)}

    # construct a heuristic Treap, still inserting keys in the order from the previous problem
    heuristic_treap = Treap()
    for k in keys:
        heuristic_treap.insert(k, heuristic_key_map[k])

    # print out the resulting treap
    print("Heuristic Treap:")
    heuristic_treap.display()

    # time the resulting search with test data
    read_and_search(heuristic_treap, test_data_cleaned)

    print("Does using priorities corresponding to letter frequency improve the running time?")
    print("YES")

    ## Step 6

    print("Step 6")

    # construct and add keys to this new Treap
    binary_treap = Treap()
    for key in keys:
        binary_treap.insert(key, 1)

    # print out the resulting treap
    print("Binary Tree Treap:")
    binary_treap.display()

    # time the resulting search with test data
    read_and_search(binary_treap, test_data_cleaned)

    print("Does using treaps improve the running time compared to a binary search tree?")
    print("NO")

if __name__ == "__main__":
    main()
