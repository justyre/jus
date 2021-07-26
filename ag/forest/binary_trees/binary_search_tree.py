# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Binary Search Tree."""

import dataclasses

from typing import Any, Optional

from forest import metrics
from forest import tree_exceptions
from forest.binary_trees import binary_tree


@dataclasses.dataclass
class Node(binary_tree.Node):
    """Binary Search Tree node definition."""

    def display_keys(self, space: str = '\t', level: int = 0) -> None:
        """Display all the keys in a Node horizontally for clear visualization."""
        # if the node is empty, print the empty set symbol
        if self is None:
            print(space * level + '∅')
            return
        
        # if the node is a leaf, print node.key
        if self.left is None and self.right is None:
            print(space * level + str(self.key))
            return
        
        # if the node has children, show right subtree up, left subtree down
        Node.display_keys(self.right, space, level + 1)
        print(space * level + str(self.key))
        Node.display_keys(self.left, space, level + 1)

class BinarySearchTree(binary_tree.BinaryTree):
    """Binary Search Tree.
    
    Attributes
    ----------
    root: `Optional[Node]`
        The root node of the binary search tree.
    empty: `bool`
        `True` if the tree is empty; `False` otherwise.
    
    Methods
    -------
    Core Functions
    search(key: `Any`)
        Look for a node based on the given key.
    insert(key: `Any`, data: `Any`)
        Insert a (key, data) pair into a binary tree.
    delete(key: `Any`)
        Delete a node based on the given key from the binary tree.
    
    Auxiliary Functions
    get_leftmost(node: `Node`)
        Return the node whose key is the smallest from the given subtree.
    get_rightmost(node: `Node` = `None`)
        Return the node whose key is the biggest from the given subtree.
    get_successor(node: `Node`)
        Return the successor node in the in-order order.
    get_predecessor(node: `Node`)
        Return the predecessor node in the in-order order.
    get_height(node: `Optional[Node]`)
        Return the height of the given node.
    
    Examples
    --------
    >>> from trees.binary_trees import binary_search_tree
    >>> tree = binary_search_tree.BinarySearchTree()
    >>> tree.insert(key=23, data="23")
    >>> tree.insert(key=4, data="4")
    >>> tree.insert(key=30, data="30")
    >>> tree.insert(key=11, data="11")
    >>> tree.insert(key=7, data="7")
    >>> tree.insert(key=34, data="34")
    >>> tree.insert(key=20, data="20")
    >>> tree.insert(key=24, data="24")
    >>> tree.insert(key=22, data="22")
    >>> tree.insert(key=15, data="15")
    >>> tree.insert(key=1, data="1")
    >>> tree.get_leftmost().key
    1
    >>> tree.get_leftmost().data
    '1'
    >>> tree.get_rightmost().key
    34
    >>> tree.get_rightmost().data
    "34"
    >>> tree.get_height(tree.root)
    4
    >>> tree.search(24).data
    `24`
    >>> tree.delete(15)
        
    Notes
    -----
    For any of the methods and functions of this class, the average time complexity is 
    O(log N), while the worst case costs O(N).
    """
    
    def __init__(self, registry: Optional[metrics.MetricRegistry] = None) -> None:
        binary_tree.BinaryTree.__init__(self)
        
        self._metrics_enabled = True if registry else False
        if self._metrics_enabled:
            self._height_histogram = metrics.Histogram()
            registry.register(name="bst.height", metric=self._height_histogram)
    
    # Override    
    def search(self, key: Any) -> Optional[Node]:
        """Look for a node by a given key.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.search`.
        """
        current: Optional[Node] = self.root
        while current:
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                return current
        # If nothing matches key, the node does not exist in the tree
        return None
    
    # Override
    def insert(self, key: Any, data: Any) -> None:
        """Insert a (key, data) pair into the binary search tree.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.insert`.
        """
        new_node = Node(key=key, data=data)
        parent: Optional[Node] = None
        current: Optional[Node] = self.root
        while current:
            parent = current
            if new_node.key < current.key:
                current = current.left
            elif new_node.key > current.key:
                current = current.right
            else:
                raise tree_exceptions.DuplicateKeyError(key=new_node.key)
        new_node.parent = parent
        # if the tree is empty
        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
            
        if self._metrics_enabled and self.root:
            self._height_histogram.update(value=self.get_height(self.root))
    
    # Override
    def delete(self, key: Any) -> None:
        """Delete a node according to the given key.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.delete`.
        """
        # if root is not None and the node to be deleted is not None
        if self.root and (deleting_node := self.search(key=key)):
            
            # Case 1: deleting_node has no child, then replace deleting_node with None.
            # Case 2a: only one right child, then replace deleting_node with the child.
            # Together, these two cases can be seen as replacing with its right child.
            if deleting_node.left is None:
                self._transplant(
                    deleting_node=deleting_node, replacing_node=deleting_node.right
                )
            
            # Case 2b: deleting_node has only one left child
            elif deleting_node.right is None:
                self._transplant(
                    deleting_node=deleting_node, replacing_node=deleting_node.left
                )
            
            # Case 3: deleting_node has two children.  Then we need to do:
            # a. Find the leftmost node (ie the smallest one) of the right subtree.
            # b. If the right child of deleting_node is the leftmost node of the right
            #    subtree, ie the right child has no left child, then replace 
            #    deleting_node with this right child.
            # c. If the right child also has two children, do:
            #    1. Take out the leftmost node the same way as the above a).
            #    2. Take the leftmost node as the new root of the right subtree.
            #    3. Assign (deleting_node.left, deleting_node.right except for the 
            #       leftmost node) as children of the new root of the right subtree.
            else:
                replacing_node = self.get_leftmost(node=deleting_node.right)
                # Case 3c. 
                # Note: by definition of replacing_node, it cannot have a left child.
                if replacing_node.parent != deleting_node:
                    # Case 3c step 1
                    self._transplant(
                        deleting_node=replacing_node,
                        replacing_node=replacing_node.right
                    )
                    # Case 3c step 2
                    replacing_node.right = deleting_node.right
                    replacing_node.right.parent = replacing_node
                # Case 3c step 3 & Case b
                # Note: These two cases share the same code, coz the left child of 
                # these two cases are the same
                self._transplant(
                    deleting_node=deleting_node, replacing_node=replacing_node
                )
                replacing_node.left = deleting_node.left
                replacing_node.left.parent = replacing_node
            
            if self._metrics_enabled and self.root:
                self._height_histogram.update(value=self.get_height(self.root))
    
    # A static method performs some functionality related to the class, but does not 
    # require any class instance to do the work.  For the auxiliary functions, they 
    # perform operations bound to the BinarySearchTree class, not a BinarySearchTree 
    # object.  Thus, the static method definition perfectly matches the aux function.
    # Override
    @staticmethod
    def get_leftmost(node: Node) -> Node:
        """Return the leftmost node from a given subtree.
        
        The key of the leftmost node is the smallest key in the given subtree.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.get_leftmost`.
        """
        current_node: Node = node
        while current_node.left:
            current_node = current_node.left
        return current_node
    
    # Override
    @staticmethod
    def get_rightmost(node: Node) -> Node:
        """Return the rightmost node from a given subtree.
        
        The key of the rightmost node is the largest key in the given subtree.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.get_rightmost`.
        """
        current_node: Node = node
        while current_node.right:
            current_node = current_node.right
        return current_node
    
    # Override
    @staticmethod
    def get_predecessor(node: Node) -> Optional[Node]:
        """Return the predecessor in the in-order order.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.get_predecessor`.
        """
        # Case 1: left child is not empty
        if node.left:
            return BinarySearchTree.get_rightmost(node=node.left)
        # Case 2: left child is empty
        parent = node.parent
        # Move up until node is the right child, and return its parent
        while parent and (node == parent.left):
            node = parent
            parent = parent.parent
        return parent
    
    # Override
    @staticmethod
    def get_successor(node: Node) -> Optional[Node]:
        """Return the successor in the in-order order.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.get_successor`.
        """
        # Case 1: right child is not empty
        if node.right:
            return BinarySearchTree.get_leftmost(node=node.right)
        # Case 2: right child is empty
        parent = node.parent
        # Move up until node is the left child, and return its parent
        while parent and (node == parent.right):
            node = parent
            parent = parent.parent
        return parent
    
    # Override
    @staticmethod
    def get_height(node: Optional[Node]) -> int:
        """Get the height of the given subtree.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.get_height`.
        """
        if node is None:
            return 0
        if node.left is None and node.right is None:
            return 0
        return max(
            BinarySearchTree.get_height(node=node.left), 
            BinarySearchTree.get_height(node=node.right)
        ) + 1
    
    def _transplant(self, deleting_node: Node, replacing_node: Optional[Node]) -> None:
        # An internal function (thus not requiring a docstring & is defined with 
        # a leading underscore) to replace the subtree rooted at `deleting_node` with 
        # the subtree rooted at `replacing_node`.
        # Note: By definition, this function has established all connections ABOVE 
        # `old d/new r` node, ie it has already set `r.parent = d.parent`. But this 
        # function does not consider whether putting r in d's place preserves BST.
        
        if deleting_node.parent is None:
            self.root = replacing_node
        elif deleting_node == deleting_node.parent.left:
            deleting_node.parent.left = replacing_node
        else:
            deleting_node.parent.right = replacing_node
        # if replacing_node is not None, point it to the orig deleting_node's parent 
        if replacing_node:
            replacing_node.parent = deleting_node.parent

