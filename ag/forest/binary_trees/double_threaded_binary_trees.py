# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Double Threaded Binary Search Trees."""

import dataclasses
from typing import Any, Optional

from forest import tree_exceptions
from forest.binary_trees import binary_tree

@dataclasses.dataclass
class Node(binary_tree.Node):
    """Double Threaded Tree node definition."""

    left: Optional["Node"] = None
    right: Optional["Node"] = None
    parent: Optional["Node"] = None
    left_thread: bool = False
    right_thread: bool = False

    def display_keys(self, tree, space: str = '\t', level: int = 0) -> None:
        """Display all the keys in a Node horizontally for clear visualization.
        
        For threaded trees, also display each node's `left/right_thread` boolean value.
        
        Notes
        -----
        For threaded trees, this function does not follow threads, because it will  
        result in RecursionError (maximum recursion depth exceeded).
        """
        # if the node is empty, print the empty set symbol
        if self is None:
            print(space * level + '∅')
            return
        
        # if the node is a leaf, print node.key
        if self.left is None and self.right is None:
            print(space * level, str(self.key), str(self.left_thread)[0], str(self.right_thread)[0])
            return
        
        # if the node has children, show right subtree up, left subtree down
        if isinstance(tree, DoubleThreadedBinaryTree):
            if not self.right_thread:
                Node.display_keys(self.right, tree, space, level + 1)
            print(space * level, str(self.key), str(self.left_thread)[0], str(self.right_thread)[0])
            if not self.left_thread:
                Node.display_keys(self.left, tree, space, level + 1)
        else:
            raise RuntimeError("Sorry, Node.display_keys() has not been implemented for this class of trees.")


class DoubleThreadedBinaryTree(binary_tree.BinaryTree):
    """Double Threaded Binary Tree.
    
    Attributes
    ----------
    root: `Optional[Node]`
        The root node of the double threaded binary search tree.
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
        
    Traversal Functions
    inorder_traverse()
        Reverse in-order traversal (LDR) by using the right threads.
    preorder_traverse()
        Pre-order traversal (DLR) by using the right threads.
    reverse_inorder_traverse()
        Reversed in-order traversal (RDL) by using the left threads.
        
    Examples
    --------
    >>> from trees.binary_trees import threaded_binary_tree
    >>> tree = threaded_binary_tree.DoubleThreadedBinaryTree()
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
    >>> [item for item in tree.inorder_traverse()]
    [(1, '1'), (4, '4'), (7, '7'), (11, '11'), (15, '15'), (20, '20'),
     (22, '22'), (23, '23'), (24, '24'), (30, '30'), (34, '34')]
    >>> [item for item in tree.preorder_traverse()]
    [(1, '1'), (4, '4'), (7, '7'), (11, '11'), (15, '15'), (20, '20'),
     (22, '22'), (23, '23'), (24, '24'), (30, '30'), (34, '34')]
    >>> [item for item in tree.reverse_inorder_traverse()]
    [(34, "34"), (30, "30"), (24, "24"), (23, "23"), (22, "22"),
     (20, "20"), (15, "15"), (11, "11"), (7, "7"), (4, "4"), (1, "1")]
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
    
    # For a double threaded BST, if a node's left attr is empty, it points to the 
    # node's predecessor; if its right attr is empty, it points to its successor.
    # 
    # Its advantage over normal un-threaded BST:
    # 1. Fast successor and predecessor access.
    # 2. No auxiliary stack or recursion approach for in-order, pre-order, and reverse-
    #    in-order traversals.
    # 3. Since no auxiliary stack or recursion is required, memory consumption is lower.
    # 4. Utilize wasted space.
    
    def __init__(self) -> None:
        binary_tree.BinaryTree.__init__(self)
    
    # Override
    def search(self, key: Any) -> Optional[Node]:
        """Look for a node by a given key.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.search`.
        """
        current = self.root
        while current:
            if key == current.key:
                return current
            elif key < current.key:
                if current.left_thread:
                    break
                current = current.left
            else:
                # When key > current.key:
                # If current is a right thread, it may have only a left child, no 
                # children at all (ie a leaf), and it cannot be the rightmost node.
                # In any case, we cannot go down right any more, so we break out of loop
                # Note: `break` terminates the innermost loop it is in (here while c)
                if current.right_thread:
                    break
                current = current.right
        return None
    
    # Override
    def insert(self, key: Any, data: Any) -> None:
        """Insert a (key, data) pair into the binary search tree.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.insert`.
        """
        node = Node(key=key, data=data)
        if self.root is None:
            self.root = node
        else:
            current: Optional[Node] = self.root
            
            while current:
                # Move to left subtree
                if node.key < current.key:
                    if current.left and not current.left_thread:
                        current = current.left
                        continue
                    else:
                        # c cannot go down left anymore, so we put node at c.l
                        node.left = current.left
                        current.left = node
                        node.right = current
                        node.right_thread = True
                        node.parent = current
                        current.left_thread = False
                        if node.left:
                            node.left_thread = True
                        break
                
                # Move to right subtree        
                elif node.key > current.key:
                    if current.right and not current.right_thread:
                        current = current.right
                        continue
                    else:
                        node.right = current.right
                        current.right = node
                        node.left = current
                        node.left_thread = True
                        current.right_thread = False
                        node.parent = current
                        if node.right:
                            node.right_thread = True
                        break
                else:
                    raise tree_exceptions.DuplicateKeyError(key=key)
    
    # Override        
    def delete(self, key: Any) -> None:
        """Delete a node according to the given key.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.delete`.
        """
        # Recall that for a node that is right threaded, it may have:
        # only a left child; no children at all (ie a leaf); and it cannot be the 
        # rightmost node.
        # For a node that is not right threaded, it may have:
        # only a right child; with both children; or it is the rightmost node.        
        if self.root and (deleting_node := self.search(key=key)):
            
            # Case 1: deleting_node has no child    
            if (deleting_node.left is None or deleting_node.left_thread) and (
                deleting_node.right is None or deleting_node.right_thread
            ):
                self._transplant(deleting_node=deleting_node, replacing_node=None)
                    
            # Case 2a: d has only a right child
            elif (deleting_node.left is None or deleting_node.left_thread) and (
                not deleting_node.right_thread
            ):
                successor = self.get_successor(node=deleting_node)
                if successor:
                    successor.left = deleting_node.left
                self._transplant(
                    deleting_node=deleting_node, replacing_node=deleting_node.right
                )
                
            # Case 2b: d has only a left child
            elif (deleting_node.right is None or deleting_node.right_thread) and (
                not deleting_node.left_thread
            ):
                predecessor = self.get_predecessor(node=deleting_node)   
                if predecessor:
                    predecessor.right = deleting_node.right
                self._transplant(
                    deleting_node=deleting_node, replacing_node=deleting_node.left
                )
                
            # Case 3: d has both left and right children
            elif deleting_node.left and deleting_node.right:
                predecessor = self.get_predecessor(node=deleting_node)
                replacing_node: Node = self.get_leftmost(node=deleting_node.right)
                successor = self.get_successor(node=replacing_node)
                # If the smallest of d.r is not d's direct child, then we turn it into 
                # d's direct right child first.
                if replacing_node.parent != deleting_node:
                    # Since r is the smallest (leftmost) of d.r, r has no left child. 
                    # So r only has a direct right child, or r is right threaded
                    if replacing_node.right_thread:
                        self._transplant(
                            deleting_node=replacing_node, replacing_node=None
                        )
                    else:
                        self._transplant(
                            deleting_node=replacing_node, 
                            replacing_node=replacing_node.right
                        )
                    replacing_node.right = deleting_node.right
                    replacing_node.right.parent = replacing_node
                    replacing_node.right_thread = False
                    
                self._transplant(
                    deleting_node=deleting_node, replacing_node=replacing_node
                )
                replacing_node.left = deleting_node.left
                replacing_node.left.parent = replacing_node
                replacing_node.left_thread = False
                # Since d has a direct right child, d's predecessor (if exists) cannot 
                # be the rightmost node. So if p is not threaded, it must have a right 
                # child, which was d and is now r; this case has been taken care of in 
                # the above self._t(d,r). And if predecessor is None, we are done. 
                # So we only need to consider when p exists and is threaded
                if predecessor and predecessor.right_thread:
                    predecessor.right = replacing_node
                if successor and successor.left_thread:
                    successor.left = replacing_node            
            
            else:
                raise RuntimeError("PLEASE CHECK! Invalid case. Should never happen.")
        
            # For all cases above, we'd better reset left&rightmost node to non-threaded
            self.get_leftmost(node=self.root).left_thread = False
            self.get_rightmost(node=self.root).right_thread = False

    # Override
    @staticmethod
    def get_leftmost(node: Node) -> Node:
        """Return the leftmost node from a given subtree.
        
        The key of the leftmost node is the smallest key in the given subtree.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.get_leftmost`.
        """
        current_node = node
        while current_node.left and not current_node.left_thread:
            current_node = current_node.left
        return current_node    
    
    # Override
    @staticmethod
    def get_rightmost(node: Node) -> Node:
        """Return the rightmost node from a given subtree.
        
        The key of the rightmost node is the biggest key in the given subtree.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.get_rightmost`.
        """
        current_node = node
        # Note: we only track down c.r if current is not threaded; otherwise we would 
        # be tracking down current's successor, which is meaningless.
        # If there is a node that has None right child and is not threaded, then it 
        # must be the rightmost node, for if it were not, it would have a `righter` (ie 
        # bigger) successor node, making it threaded.
        while current_node.right and not current_node.right_thread:
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
        if node.left_thread:
            return node.left
        else:
            # If node has left child, then its predecessor is the biggest of left child
            if node.left:
                return DoubleThreadedBinaryTree.get_rightmost(node=node.left)
            return None

    # Override
    @staticmethod
    def get_successor(node: Node) -> Optional[Node]:
        """Return the successor in the in-order order.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.get_successor`.
        """
        # If node is right threaded, n.r is its successor
        if node.right_thread:
            return node.right
        else:
            if node.right:
                return DoubleThreadedBinaryTree.get_leftmost(node=node.right)
            # If node is not a thread and n.r is None, its successor is None
            return None
    
    # Override        
    @staticmethod
    def get_height(node: Optional[Node]) -> int:
        """Get the height of the given subtree.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.get_height`.
        """
        # All nodes that are not threads, either they are with a right child, with both 
        # children, or the rightmost node whose right child is None.
        if node is None:
            return 0
        if (
            (node.left is None and node.right is None)
            or (node.left is None and node.right_thread)
            or (node.right is None and node.left_thread)
            or (node.right_thread and node.left_thread) 
        ):
            return 0
        if node.left is not None and node.right_thread:
            return DoubleThreadedBinaryTree.get_height(node.left) + 1
        if node.right is not None and node.left_thread:
            return DoubleThreadedBinaryTree.get_height(node.right) + 1
        return max(
            DoubleThreadedBinaryTree.get_height(node.left),
            DoubleThreadedBinaryTree.get_height(node.right)
        ) + 1
        # ANOTHER IMPLEMENTATION FOR THIS:
        # if node:        
        #     if not node.left_thread and not node.right_thread:
        #         return max(
        #             DoubleThreadedBinaryTree.get_height(node.left),
        #             DoubleThreadedBinaryTree.get_height(node.right),
        #         ) + 1
        #     if node.left_thread and not node.right_thread:
        #         return DoubleThreadedBinaryTree.get_height(node.right) + 1
        #     if not node.left_thread and node.right_thread:
        #         return DoubleThreadedBinaryTree.get_height(node.left) + 1
        # # Note: If node is None, return 0; if node is a leaf, although it goes into the 
        # # previous `if`, it satisfies none of the three sub-if conditions, so return 0
        # return 0

    def inorder_traverse(self) -> binary_tree.Pairs:
        """Use the right threads to traverse the tree in in-order order (LDR).
        
        Yields
        ------
        `Pairs`
            The next (key, data) pair in the tree in-order traversal.
        """
        if self.root:
            current: Optional[Node] = self.get_leftmost(node=self.root)
            while current:
                yield (current.key, current.data)
                if current.right_thread:
                    current = current.right
                else:
                    # If current is not threaded, and c.r is None, it's rightmost
                    if current.right is None:
                        break
                    # If c.r exists, we move on to the leftmost of c.r
                    current = self.get_leftmost(current.right)
    
    def preorder_traverse(self) -> binary_tree.Pairs:
        """Use the right threads to traverse the tree in pre-order order (DLR).
        
        Yields
        ------
        `Pairs`
            The next (key, data) pair in the tree pre-order traversal.
        """
        current = self.root
        while current:
            yield (current.key, current.data)
                
            if current.left is not None and not current.left_thread:
                current = current.left
            elif current.right_thread:
                # If c.l is None, left side is exhausted, so we move up c.r.r... 
                # until we find a node that is non-thread. Then we go to its right.
                while current.right_thread:
                    current = current.right
                current = current.right
            else:
                # If c.l is None and c is non-thread, then c.r exists, so we get that
                current = current.right

    def reverse_inorder_traverse(self) -> binary_tree.Pairs:
        """Use the left threads to traverse the tree in reversed in-order order (RDL).
        
        Yields
        ------
        `Pairs`
            The next (key, data) pair in the tree reversed in-order traversal.
        """
        if self.root:
            current: Optional[Node] = self.get_rightmost(node=self.root)
            while current:
                yield (current.key, current.data)
                if current.left_thread:
                    current = current.left
                else:
                    # If current is not threaded, and c.l is None, it's leftmost
                    if current.left is None:
                        break
                    # If c.l exists, we move on to the rightmost of c.l
                    current = self.get_rightmost(current.left)

    def _transplant(self, deleting_node: Node, replacing_node: Optional[Node]) -> None:
        # An internal function (thus not requiring a docstring & is defined with 
        # a leading underscore) to replace the subtree rooted at `deleting_node` with 
        # the subtree rooted at `replacing_node`. replacing_node may be None.
        # Note: By definition, this function has established all connections ABOVE 
        # `old d/new r` node, ie it has already set `r.parent = d.parent`. But this 
        # function does not consider whether putting r in d's place preserves BST.
        # Also, when deleting d, we delete the whole subtree rooted at d, and replace 
        # it with a whole new subtree rooted at r.
        
        if deleting_node.parent is None:
            self.root = replacing_node
            # If self.root (ie replacing_node) exists, then either it has a left  
            # child (is_thread False), or its left child is None (ie self.root is the 
            # leftmost node, so is_thread False).
            if self.root:                
                self.root.left_thread = False
                self.root.right_thread = False
        elif deleting_node == deleting_node.parent.left:
            # If d is its parent's left child
            deleting_node.parent.left = replacing_node
            if replacing_node:
                if deleting_node.left_thread and replacing_node.left_thread:
                    replacing_node.left = deleting_node.left
                if deleting_node.right_thread and replacing_node.right_thread:
                    replacing_node.right = deleting_node.right
            else:
                deleting_node.parent.left = deleting_node.left
                deleting_node.parent.left_thread = True                            
        else:
            # If d is its parent's right child
            deleting_node.parent.right = replacing_node
            if replacing_node:
                if deleting_node.left_thread and replacing_node.left_thread:
                    replacing_node.left = deleting_node.left
                if deleting_node.right_thread and replacing_node.right_thread:
                    replacing_node.right = deleting_node.right
            else:
                deleting_node.parent.right = deleting_node.right
                deleting_node.parent.right_thread = True
        
        # fix the pointer to parent
        if replacing_node:
            replacing_node.parent = deleting_node.parent


# # test client

# tree = DoubleThreadedBinaryTree()
# print(DoubleThreadedBinaryTree.get_height(tree.root))  # Test None case, should be 0
# tree.insert(key=4, data="")
# tree.insert(key=1, data="")
# tree.insert(key=7, data="")
# tree.insert(key=3, data="")
# tree.insert(key=5, data="")
# tree.insert(key=8, data="")
# tree.insert(key=2, data="")
# # tree.insert(key=2.5, data="")
# tree.insert(key=6, data="")
# print(tree.search(6).parent)
# print(DoubleThreadedBinaryTree.get_height(tree.search(1)))
# print("Before deleting: ")
# tree.root.display_keys(tree)
# print(list(tree.inorder_traverse()))
# print(list(tree.preorder_traverse()))

# tree.delete(7)
# print("After deleting: ")
# tree.root.display_keys(tree)
# print(list(tree.preorder_traverse()))
# print(tree.search(3).right.key)
# print()

# tree = DoubleThreadedBinaryTree()
# tree.insert(key=4, data="")
# tree.insert(key=1, data="")
# tree.insert(key=7, data="")
# tree.insert(key=3, data="")
# tree.insert(key=5, data="")
# tree.insert(key=8, data="")
# tree.insert(key=2, data="")
# # tree.insert(key=2.5, data="")
# tree.insert(key=6, data="")
# print("Before deleting: ")
# tree.root.display_keys(tree)
# print(list(tree.reverse_inorder_traverse()))

# tree.delete(4)
# print("After deleting: ")
# tree.root.display_keys(tree)
# print(list(tree.reverse_inorder_traverse()))
# print(tree.search(5).left.key)