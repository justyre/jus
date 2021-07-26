# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""AVL Tree."""

import dataclasses
from typing import Any, Optional

from forest import metrics
from forest import tree_exceptions
from forest.binary_trees import binary_tree

@dataclasses.dataclass
class Node(binary_tree.Node):
    """AVL Tree node definition."""
    
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    parent: Optional["Node"] = None
    # For a None node, its height is -1; for a leaf, its height is 0
    height: int = 0
    # Size of this node's subtree including itself (ie total # nodes). For None it is 0
    subtree_size: int = 1
    
    def display_keys(self, space: str = '\t', level: int = 0) -> None:
        """Display all the keys in a Node horizontally for clear visualization.
        
        For AVL trees, also display each node's height.
        """
        # if the node is empty, print the empty set symbol
        if self is None:
            print(space * level + '∅')
            return
        
        # if the node is a leaf, print node.key
        if self.left is None and self.right is None:
            print(space * level, str(self.key), str(self.height))
            return
        
        # if the node has children, show right subtree up, left subtree down
        Node.display_keys(self.right, space, level + 1)
        print(space * level, str(self.key), str(self.height))
        Node.display_keys(self.left, space, level + 1)

class AVLTree(binary_tree.BinaryTree):
    """AVL Tree.
    
    Attributes
    ----------
    root: `Optional[Node]`
        The root node of the red-black tree.
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
    get_rightmost(node: `Node`)
        Return the node whose key is the biggest from the given subtree.
    get_successor(node: `Node`)
        Return the successor node in the in-order order.
    get_predecessor(node: `Node`)
        Return the predecessor node in the in-order order.
    get_height(node: `Optional[Node]`)
        Return the height of the given node.
        
    Examples
    --------
    >>> from trees.binary_trees import avl_tree
    >>> tree = avl_tree.AVLTree()
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
    """
    
    # As a kind of self-balancing BST, all the methods of this class are O(log N).
    #
    # COMPARISON OF AVL TREE AGAINST RED-BLACK TREE
    # 
    # Since the red-black tree ensures that no path is twice longer than other paths, 
    # whereas the AVL tree guarantees that for any node, the heights of its left subtree
    # and its right subtree differ by at most one. 
    # Therefore, the AVL tree is more balanced than the red-black tree, ie shallower.
    # 
    # For search, the worst case takes O(h) (h is height of tree), so AVL is better.
    # For insertion, we first spend O(h) finding the place for insertin, and then do 
    # rotations that take O(1). AVL and red-black are the same.
    # For deletion, we first spend O(h) finding the place for deletion, and then do 
    # rotations. Whereas red-black tree takes O(1) (const) max number of rotations, 
    # AVL can take up to O(h) rotations. So red-black tree is better.
    # Both AVL and red-black trees have O(n) space usage. Although the color info bit 
    # is smaller than AVL's height info bit (an integer), for ints not too big, in 
    # Python, both types cost 28 bytes (which can be checked with sys.getsizeof()). 
    # However, in other languages, the size could be quite different. For example, in 
    # C++, color R or B can be stored as a char which is 1 byte (=8 bits), while height 
    # is an int that coests 4 bytes (=32 bits).
    
    def __init__(self, registry: Optional[metrics.MetricRegistry] = None) -> None:
        binary_tree.BinaryTree.__init__(self)
        self.inversion_count: int = 0
        
        self._metrics_enabled = True if registry else False
        if self._metrics_enabled:
            self._rotate_counter = metrics.Counter()
            self._height_histogram = metrics.Histogram()
            registry.register(name="avlt.rotate", metric=self._rotate_counter)
            registry.register(name="avlt.height", metric=self._height_histogram)
    
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
        # if nothing matches key, the node does not exist in the tree
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
                
                # First, update c.r's subtree_size, since it may be stale from last loop
                if current.right is not None:
                    current.right.subtree_size = 1 + self.get_subtree_size(current.right.left) + self.get_subtree_size(current.right.right)
                # To count inversions, for each inserted node, we need to find number of
                # elems greater than `key` that have been inserted before `key`.
                # Whenever new_node < c, we go down left a level, so inversion_count 
                # increases by 1(current) + c.right.
                # Note: Here we only consider first-time insertion of a list into an 
                # empty tree. Subsequent delete/insert does not alter inversion_count.
                self.inversion_count += 1 + self.get_subtree_size(current.right)
                
                current = current.left                    
            elif new_node.key > current.key:
                current = current.right
            else:
                raise tree_exceptions.DuplicateKeyError(key=new_node.key)
        new_node.parent = parent
        # if the tree is empty
        if parent is None:
            self.root = new_node
        else:
            if new_node.key < parent.key:
                parent.left = new_node
            else:
                parent.right = new_node
            # After insertion, fix the broken AVL tree property.
            # If the parent has two children after insertion, it means that the parent 
            # had one child before. In this case, AVL tree property (balance factor is 
            # -1, 0, 1) is maintained, so no fixup (ie height update) is needed.
            if not (parent.left and parent.right):
                self._insert_fixup(new_node)
        
        if self._metrics_enabled:
            self._height_histogram.update(value=self.get_height(self.root))
    
    # Override    
    def delete(self, key: Any) -> None:
        """Delete a node according to the given key.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.delete`.
        """
        # If root is not None and the node to be deleted is not None
        if self.root and (deleting_node := self.search(key=key)):
            
            # Case 1: deleting_node has no child
            if deleting_node.left is None and deleting_node.right is None:
                self._delete_no_child(deleting_node=deleting_node)
            
            # Case 2: deleting_node has two children
            elif deleting_node.left and deleting_node.right:
                replacing_node = self.get_leftmost(node=deleting_node.right)
                # Replace d with r, but keep r in place for later deletion
                deleting_node.key = replacing_node.key
                deleting_node.data = replacing_node.data
                # Since r is leftmost of d.r, r cannot have a left child.
                # So r can either have a right child, or no child at all.
                if replacing_node.right:
                    self._delete_one_child(deleting_node=replacing_node)
                else:
                    self._delete_no_child(deleting_node=replacing_node)
                    
            # Case 3: deleting_node has only one child.
            else:
                self._delete_one_child(deleting_node=deleting_node)
            
            if self._metrics_enabled:
                self._height_histogram.update(value=self.get_height(self.root))
    
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
            return AVLTree.get_rightmost(node=node.left)
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
            return AVLTree.get_leftmost(node=node.right)
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
        if node:
            return node.height
        # For AVL trees, we define the height of a None node to be -1
        return -1
    
    def _get_balance_factor(self, node: Optional[Node]) -> int:
        # The balance factor of a node := height(left subtree) - height(right subtree).
        if node:
            return self.get_height(node.left) - self.get_height(node.right)
        # For AVL trees, a None node has height -1 and balance factor -1
        return -1
    
    def _left_rotate(self, node_x: Node) -> None:
        # Left rotate node_x down and node_x.right up a level as the new subtree root.
        node_x_right = node_x.right
        if node_x_right is None:
            raise RuntimeError("Invalid left rotate: node_x.right cannot be None")
        
        # Turn nxr.l to nx.r
        node_x.right = node_x_right.left
        if node_x_right.left is not None:
            node_x_right.left.parent = node_x
            # If nxr.l was a NIL, there is no need to set its parent (NILs have no dads)
        node_x_right.parent = node_x.parent
        
        # We need to decide where to hang nxr, which depends on the relation between 
        # nx and nx.pa: If nx.pa was a Leaf, nxr gets to be the new root. If nx was the 
        # left child of nx.pa, nxr should be nx.pa's new left child. Same if right child
        if node_x.parent is None:
            # If nx.pa was a Leaf, nxr is the new root
            self.root = node_x_right
        elif node_x == node_x.parent.left:
            node_x.parent.left = node_x_right
        else:
            node_x.parent.right = node_x_right
            
        # Now hang nx as nxr.l
        node_x_right.left = node_x
        node_x.parent = node_x_right
        
        # Set new heights
        node_x.height = 1 + max(
            self.get_height(node_x.left), self.get_height(node_x.right)
        )
        node_x_right.height = 1 + max(
            self.get_height(node_x_right.left), self.get_height(node_x_right.right)
        )
        
        # Update sizes
        node_x.subtree_size = 1 + self.get_subtree_size(node_x.left) + self.get_subtree_size(node_x.right)
        node_x_right.subtree_size = 1 + self.get_subtree_size(node_x_right.left) + self.get_subtree_size(node_x_right.right)
        
        if self._metrics_enabled:
            self._rotate_counter.increase()
    
    def _right_rotate(self, node_x: Node) -> None:
        # Right rotate node_x down and node_x.left up a level as the new subtree root.
        node_x_left = node_x.left
        if node_x_left is None:
            raise RuntimeError("Invalid right rotate: node_x.left cannot be a Leaf")
        
        # Turn nxl.r to nx.l
        node_x.left = node_x_left.right
        if node_x_left.right is not None:
            node_x_left.right.parent = node_x
        node_x_left.parent = node_x.parent
        
        if node_x.parent is None:
            self.root = node_x_left
        elif node_x == node_x.parent.left:
            node_x.parent.left = node_x_left
        else:
            node_x.parent.right = node_x_left
        
        # Now hang nx as nxl.r
        node_x_left.right = node_x
        node_x.parent = node_x_left
        
        # Set new heights
        node_x.height = 1 + max(
            self.get_height(node_x.left), self.get_height(node_x.right)
        )
        node_x_left.height = 1 + max(
            self.get_height(node_x_left.left), self.get_height(node_x_left.right)
        )
        
        # Update sizes
        node_x.subtree_size = 1 + self.get_subtree_size(node_x.left) + self.get_subtree_size(node_x.right)
        node_x_left.subtree_size = 1 + self.get_subtree_size(node_x_left.left) + self.get_subtree_size(node_x_left.right)
        
        if self._metrics_enabled:
            self._rotate_counter.increase()

    def _insert_fixup(self, new_node: Node) -> None:
        # Fix up after the insertion to restore the AVL tree property,
        # ie to ensure that all nodes have a balance factor of -1, 0, 1.
        parent = new_node.parent
        while parent:
            # set the current pa's height while traveling up back to the root
            parent.height = 1 + max(
                self.get_height(parent.left), self.get_height(parent.right)
            )
            grandparent = parent.parent
            if grandparent:
                # Solve the imbalance
                if self._get_balance_factor(grandparent) > 1:
                    if self._get_balance_factor(parent) < 0:
                        # Case left-right.
                        # Do a left rotate to turn it into Case left-left
                        self._left_rotate(parent)
                    # Case left-left
                    self._right_rotate(grandparent)
                    # For an insertion, after these rotations, the height of grandpa is
                    # the same as before the insertion. So this fixup does not affect 
                    # the balancedness of grandparent's parent or any node higher up, 
                    # meaning that we can exit the while loop safely
                    break
                elif self._get_balance_factor(grandparent) < -1:
                    if self._get_balance_factor(parent) > 0:
                        # Case right-left
                        # Do a right rotate to turn it into Case right-right
                        self._right_rotate(parent)
                    # Case right-right
                    self._left_rotate(grandparent)
                    break
            
            parent = parent.parent
    
    def _delete_fixup(self, fixing_node: Node) -> None:
        # Fix up after the deletion to restore the AVL tree property.
        # The algorithm is quite similar to _insert_fixup().
        while fixing_node:
            fixing_node.height = 1 + max(
                self.get_height(fixing_node.left), self.get_height(fixing_node.right)
            )
            if self._get_balance_factor(fixing_node) > 1:
                # Since fn's bf > 1, it must have a left child
                if self._get_balance_factor(fixing_node.left) < 0:
                    # Case left-right.
                    # Do a left rotate to turn it into Case left-left.
                    self._left_rotate(fixing_node.left)
                # Case left-left
                self._right_rotate(fixing_node)
                # Note: Unlike _insert_fixup(), the unbalanced bf may propagate above 
                # fn (because the height of fn may change after the deletion). 
                # Therefore, after restoring the bottommost unbalanced node fn, 
                # we need to go on to check if its parent is unbalanced, and fix it too,
                # all the way up until we reach the root and make the root balanced.
                # So we cannot break out of the while loop.
            
            elif self._get_balance_factor(fixing_node) < -1:
                # Since fn's bf < -1, it must have a right child
                if self._get_balance_factor(fixing_node.right) > 0:
                    # Case right-left
                    # Do a right rotate to turn it into Case right-right
                    self._right_rotate(fixing_node.right)
                # Case right-right
                self._left_rotate(fixing_node)
            
            fixing_node = fixing_node.parent
                    
    
    def _delete_no_child(self, deleting_node: Node) -> None:
        # Delete a node who has no child.
        parent = deleting_node.parent
        self._transplant(deleting_node=deleting_node, replacing_node=None)
        if parent:
            self._delete_fixup(fixing_node=parent)
    
    def _delete_one_child(self, deleting_node: Node) -> None:
        # Delete a node who has only one child.
        parent = deleting_node.parent
        replacing_node: Node = (
            deleting_node.right if deleting_node.right else deleting_node.left
        )
        self._transplant(deleting_node=deleting_node, replacing_node=replacing_node)
        if parent:
            self._delete_fixup(fixing_node=parent)

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
    
    @staticmethod
    def get_subtree_size(node: Optional[Node]) -> int:
        """Get the size of the subtree rooted with `node`, including `node` itself."""
        return 0 if node is None else node.subtree_size