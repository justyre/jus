# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Single Threaded Binary Search Trees."""

import dataclasses
from typing import Any, Optional

from forest import tree_exceptions
from forest.binary_trees import binary_tree

@dataclasses.dataclass
class Node(binary_tree.Node):
    """Single Threaded Tree node definition."""

    left: Optional["Node"] = None
    right: Optional["Node"] = None
    parent: Optional["Node"] = None
    is_thread: bool = False

    def display_keys(self, tree, space: str = '\t', level: int = 0) -> None:
        """Display all the keys in a Node horizontally for clear visualization.
        
        For threaded trees, also display each node's `is_thread` boolean value.
        
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
            print(space * level, str(self.key), str(self.is_thread)[0])
            return
        
        # if the node has children, show right subtree up, left subtree down
        if isinstance(tree, RightThreadedBinaryTree):
            if not self.is_thread:
                Node.display_keys(self.right, tree, space, level + 1)
            print(space * level, str(self.key), str(self.is_thread)[0])
            Node.display_keys(self.left, tree, space, level + 1)
        elif isinstance(tree, LeftThreadedBinaryTree):
            Node.display_keys(self.right, tree, space, level + 1)
            print(space * level, str(self.key), str(self.is_thread)[0])
            if not self.is_thread:
                Node.display_keys(self.left, tree, space, level + 1)
        else:
            raise RuntimeError("Sorry, Node.display_keys() has not been implemented for this class of trees.")

class RightThreadedBinaryTree(binary_tree.BinaryTree):
    """Right Threaded Binary Tree.
    
    Attributes
    ----------
    root: `Optional[Node]`
        The root node of the right threaded binary search tree.
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
        
    Traversal Functions
    inorder_traverse()
        Reverse in-order traversal (LDR) by using the right threads.
    preorder_traverse()
        Pre-order traversal (DLR) by using the right threads.
    
    Examples
    --------
    >>> from trees.binary_trees import threaded_binary_tree
    >>> tree = threaded_binary_tree.RightThreadedBinaryTree()
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
    
    # In a left single-threaded binary tree, the empty right attribute of a node 
    # points to the node's successor, its is_thread is True, and any empty left 
    # attributes remain empty.
    # Note: There is an important exception: the rightmost node's right attr remains 
    # empty, and its is_thread is False.
    # From the above definition, we can deduce that all nodes that are threads are 
    # "nodes with no direct right child (except for the rightmost node)", 
    # of which there are two kinds: 
    # 1. leaf nodes (which has no direct left or right child), or 
    # 2. "nodes with only a left child".
    # All nodes that are not threads, either they are with a right child, with both 
    # children, or the rightmost node.
    # Note 2: Adding threads to BST makes its implementation more complicated, but they 
    # could be a solution when "traversals are critical but space consumption is 
    # concerned".
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
                current = current.left
            else:
                # When key > current.key:
                # If current is a right thread, it may have only a left child, no 
                # children at all (ie a leaf), and it cannot be the rightmost node.
                # In any case, we cannot go down right any more, so we break out of loop
                if current.is_thread:
                    break
                current = current.right
        return None
    
    # Override
    def insert(self, key: Any, data: Any) -> None:
        """Insert a (key, data) pair into the right threaded binary search tree.
        
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
                # If current is a right thread, it may have only a left child, no 
                # children at all (ie a leaf), and it cannot be the rightmost node.
                # In any case, we cannot go down right any more, so we break out of loop
                if current.is_thread:
                    break  # this line is equivalent to `current = None`
                else:
                    current = current.right
            else:
                raise tree_exceptions.DuplicateKeyError(key=new_node.key)
        
        new_node.parent = parent
        # If the tree is empty
        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
            # Update thread. Since a new node has no children, it must be a thread
            new_node.right = parent
            new_node.is_thread = True
        else:
            # When new_node is the new right child of parent:
            # If the parent was a thread, it no longer is one (coz it has a right child
            # now), but new_node is a thread (with no right child; pointing to where 
            # the old parent was pointing), ie the thread pointer is passed down from 
            # parent to new_node.
            # If the parent was not a thread, parent still is not a thread, and we can 
            # do the pass-down just like above.
            new_node.is_thread = parent.is_thread
            new_node.right = parent.right
            parent.is_thread = False
            # After the update, set the parent's right child to new_node
            parent.right = new_node
    
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
            
            # Case 1: deleting_node has no left child.    
            if deleting_node.left is None:
                # If d is right threaded, then d has no actual right child, so we 
                # just replace d with None
                if deleting_node.is_thread:
                    self._transplant(
                        deleting_node=deleting_node, replacing_node=None
                    )
                else:
                    # If d is not threaded, either d is rightmost node (so d.r is None) 
                    # or d has a right child. In either case, replace d with d.r
                    self._transplant(
                        deleting_node=deleting_node, replacing_node=deleting_node.right
                    )
                    
            # Case 2: d has a left child and is threaded, or d has a left child and is 
            # the rightmost node (which has no right child by definition)
            elif deleting_node.left and (
                deleting_node.is_thread or
                deleting_node == self.get_rightmost(node=self.root)
            ):
                predecessor = self.get_predecessor(node=deleting_node)
                if predecessor:
                    predecessor.right = deleting_node.right
                self._transplant(
                    deleting_node=deleting_node, replacing_node=deleting_node.left
                )
                
            # Case 3: d has a left child and is not threaded (but d is not rightmost)
            elif deleting_node.left and not deleting_node.is_thread:
                predecessor = self.get_predecessor(node=deleting_node)
                replacing_node: Node = self.get_leftmost(node=deleting_node.right)
                # If the smallest of d.r is not d's direct child, then we turn it into 
                # d's direct right child first.
                if replacing_node.parent != deleting_node:
                    # Since r is the smallest (leftmost) of d.r, r has no left child. 
                    # So r only has a direct right child, or r is right threaded
                    if replacing_node.is_thread:
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
                    replacing_node.is_thread = False
                    
                self._transplant(
                    deleting_node=deleting_node, replacing_node=replacing_node
                )
                replacing_node.left = deleting_node.left
                replacing_node.left.parent = replacing_node
                # Since d has a direct right child, d's predecessor (if exists) cannot 
                # be the rightmost node. So if p is not threaded, it must have a right 
                # child, which was d and is now r; this case has been taken care of in 
                # the above self._t(d,r). And if predecessor is None, we are done. 
                # So we only need to consider when p exists and is threaded
                if predecessor and predecessor.is_thread:
                    predecessor.right = replacing_node            
            
            else:
                raise RuntimeError("PLEASE CHECK! Invalid case. Should never happen.")
        
            # For all cases above, we'd better reset rightmost node to non-threaded
            self.get_rightmost(node=self.root).is_thread = False
    
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
        while current_node.left:
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
        while current_node.is_thread is False and current_node.right:
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
        # If node has left child, then its predecessor is the biggest of left child
        if node.left:
            return RightThreadedBinaryTree.get_rightmost(node=node.left)
        # If node has no left child, then its predecessor is not below itself; it 
        # must be above. So we need to move up all the way until we find 
        # a parent that has node as its right child, and this parent is its predecessor
        parent = node.parent
        while parent and node == parent.left:
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
        # If node is right threaded, n.r is its successor
        if node.is_thread:
            return node.right
        else:
            if node.right:
                return RightThreadedBinaryTree.get_leftmost(node=node.right)
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
        if node.left is None and node.is_thread:
            return 0
        if node.left is not None and node.is_thread:
            return RightThreadedBinaryTree.get_height(node.left) + 1
        return max(
            RightThreadedBinaryTree.get_height(node=node.left), 
            RightThreadedBinaryTree.get_height(node=node.right)
        ) + 1
        # ANOTHER IMPLEMENTATION FOR THIS:
        # if node:        
        #     if node.left and (node.right and node.is_thread is False):
        #         return max(
        #             RightThreadedBinaryTree.get_height(node.left),
        #             RightThreadedBinaryTree.get_height(node.right),
        #         ) + 1
        #     if node.left:
        #         return RightThreadedBinaryTree.get_height(node.left) + 1
        #     if node.right and node.is_thread is False:
        #         return RightThreadedBinaryTree.get_height(node.right) + 1
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
                if current.is_thread:
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
                
            if current.left is not None:
                current = current.left
            elif current.is_thread:
                # If c.l is None, left side is exhausted, so we move up c.r.r... 
                # until we find a node that is non-thread. Then we go to its right.
                while current.is_thread:
                    current = current.right
                current = current.right
            else:
                # If c.l is None and c is non-thread, then c.r exists, so we get that
                current = current.right 
                        
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
            # If self.root (ie replacing_node) exists, then either it has a right 
            # child (is_thread False), or its right child is None (ie self.root is the 
            # rightmost node, so is_thread False).
            if self.root:                
                self.root.is_thread = False
        elif deleting_node == deleting_node.parent.left:
            # If d is its parent's left child
            deleting_node.parent.left = replacing_node
            if replacing_node and deleting_node.is_thread and replacing_node.is_thread:
                # If replacing_node is not None and both d and r are right threaded, 
                # then we just need to set d's successor to r's successor.
                # If d is not threaded, there is nothing we need to pass to r (we just
                # get rid of the whole subtree rooted at d); if d is threaded but r is 
                # not threaded, the lost d's thread should be passed down to rightmost 
                # of r.r, which is taken care of in the delete() function (remember 
                # that we only deal with everything ABOVE r/d in this function)
                replacing_node.right = deleting_node.right
        else:
            # If d is its parent's right child
            deleting_node.parent.right = replacing_node
            if replacing_node:
                if deleting_node.is_thread and replacing_node.is_thread:
                    replacing_node.right = deleting_node.right
            else:
                # If r is None, then we need to set d's successor to d.parent's 
                # successor, which also turns d.parent into a thread.
                # But there is one special case: when d.parent is the new rightmost 
                # node, d.parent should not be threaded. This is later adjusted in 
                # delete() function, because for now we don't know which is rightmost.
                deleting_node.parent.right = deleting_node.right
                deleting_node.parent.is_thread = True
        
        # fix the pointer to parent
        if replacing_node:
            replacing_node.parent = deleting_node.parent



class LeftThreadedBinaryTree(binary_tree.BinaryTree):
    """Left Threaded Binary Tree.
    
    Attributes
    ----------
    root: `Optional[Node]`
        The root node of the left threaded binary search tree.
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
        
    Traversal Functions
    reverse_inorder_traverse()
        Reversed in-order traversal (RDL) by using the left threads.
        
    Examples
    --------
    >>> from trees.binary_trees import threaded_binary_tree
    >>> tree = threaded_binary_tree.LeftThreadedBinaryTree()
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
    
    # In a right single-threaded binary tree, the empty left attribute of a node 
    # points to the node's predecessor, its is_thread is True, and any empty right  
    # attributes remain empty.
    # Note: There is an important exception: the leftmost node's left attr remains 
    # empty, and its is_thread is False.
    # From the above definition, we can deduce that all nodes that are threads are 
    # "nodes with no direct left child (except for the leftmost node)", 
    # of which there are two kinds: 
    # 1. leaf nodes (which has no direct left or right child), or 
    # 2. "nodes with only a right child".
    # All nodes that are not threads, either they are with a left child, with both 
    # children, or the leftmost node.
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
            elif key > current.key:
                current = current.right
            else:
                # When key < current.key:
                # If current is a left thread, it may have only a right child, no 
                # children at all (ie a leaf), and it cannot be the leftmost node.
                # In any case, we cannot go down left any more, so we break out of loop
                if current.is_thread:
                    break
                current = current.left
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
            if new_node.key > current.key:
                current = current.right
            elif new_node.key < current.key:
                # If current is a left thread, it may have only a right child, no 
                # children at all (ie a leaf), and it cannot be the leftmost node.
                # In any case, we cannot go down left any more, so we break out of loop
                if current.is_thread:
                    break  # this line is equivalent to `current = None`
                else:
                    current = current.left
            else:
                raise tree_exceptions.DuplicateKeyError(key=new_node.key)
        
        new_node.parent = parent
        # If the tree is empty
        if parent is None:
            self.root = new_node
        elif new_node.key > parent.key:
            parent.right = new_node
            # Update thread. Since a new node has no children, it must be a thread
            new_node.left = parent
            new_node.is_thread = True
        else:
            # When new_node is the new left child of parent:
            # If the parent was a thread, it no longer is one (coz it has a left child
            # now), but new_node is a thread (with no left child; pointing to where 
            # the old parent was pointing), ie the thread pointer is passed down from 
            # parent to new_node.
            # If the parent was not a thread, parent still is not a thread, and we can 
            # do the pass-down just like above.
            new_node.is_thread = parent.is_thread
            new_node.left = parent.left
            parent.is_thread = False
            # After the update, set the parent's left child to new_node
            parent.left = new_node
    
    # Override        
    def delete(self, key: Any) -> None:
        """Delete a node according to the given key.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.delete`.
        """
        # Recall that for a node that is left threaded, it may have:
        # only a right child; no children at all (ie a leaf); and it cannot be the 
        # leftmost node.
        # For a node that is not left threaded, it may have:
        # only a left child; with both children; or it is the leftmost node.        
        if self.root and (deleting_node := self.search(key=key)):
            
            # Case 1: deleting_node has no right child.    
            if deleting_node.right is None:
                # If d is left threaded, then d has no actual left child, so we 
                # just replace d with None
                if deleting_node.is_thread:
                    self._transplant(
                        deleting_node=deleting_node, replacing_node=None
                    )
                else:
                    self._transplant(
                        deleting_node=deleting_node, replacing_node=deleting_node.left
                    )
                    
            # Case 2: d has a right child and is threaded, or d has a right child and 
            # is the leftmost node (which has no left child by definition)
            elif deleting_node.right and (
                deleting_node.is_thread or
                deleting_node == self.get_leftmost(node=self.root)
            ):
                successor = self.get_successor(node=deleting_node)
                if successor:
                    successor.left = deleting_node.left
                self._transplant(
                    deleting_node=deleting_node, replacing_node=deleting_node.right
                )
                
            # Case 3: d has a right child and is not threaded (but d is not leftmost)
            elif deleting_node.right and not deleting_node.is_thread:
                replacing_node: Node = self.get_leftmost(node=deleting_node.right)
                successor = self.get_successor(node=replacing_node)
                # If the smallest of d.r is not d's direct child, then we turn it into 
                # d's direct right child first.
                if replacing_node.parent != deleting_node:
                    # Since r is the smallest (leftmost) of d.r, r has no left child. 
                    # So r must be left threaded.
                    self._transplant(
                        deleting_node=replacing_node, 
                        replacing_node=replacing_node.right
                    )
                    replacing_node.right = deleting_node.right
                    replacing_node.right.parent = replacing_node
                    
                self._transplant(
                    deleting_node=deleting_node, replacing_node=replacing_node
                )
                replacing_node.left = deleting_node.left
                replacing_node.left.parent = replacing_node
                replacing_node.is_thread = False
                
                # Since r is the leftmost of d.r, r's successor (if exists) cannot 
                # be the leftmost of d.r. Either s is r.r, or s is r.parent (ie r is 
                # s's left child).  
                if successor and successor.is_thread:
                    successor.left = replacing_node            
            
            else:
                raise RuntimeError("PLEASE CHECK! Invalid case. Should never happen.")
        
            # For all cases above, we'd better reset leftmost node to non-threaded
            self.get_leftmost(node=self.root).is_thread = False
    
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
        while current_node.left and not current_node.is_thread:
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
        # If node is left threaded, n.l is its predecessor
        if node.is_thread:
            return node.left
        else:
            if node.right:
                return LeftThreadedBinaryTree.get_rightmost(node=node.left)
            # If node is not a thread and n.l is None, its predecessor is None
            return None

    # Override
    @staticmethod
    def get_successor(node: Node) -> Optional[Node]:
        """Return the successor in the in-order order.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.get_successor`.
        """
        # If node has right child, then its successor is the smallest of right child
        if node.right:
            return LeftThreadedBinaryTree.get_leftmost(node=node.right)
        # If node has no right child, then its successor is not below itself; it 
        # must be above. So we need to move up all the way until we find 
        # a parent that has node as its left child, and this parent is its successor
        parent = node.parent
        while parent and node == parent.right:
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
        # All nodes that are not threads, either they are with a left child, with both 
        # children, or the leftmost node whose left child is None.
        if node is None:
            return 0
        if node.right is None and node.is_thread:
            return 0
        if node.right is not None and node.is_thread:
            return LeftThreadedBinaryTree.get_height(node.right) + 1
        return max(
            LeftThreadedBinaryTree.get_height(node=node.left), 
            LeftThreadedBinaryTree.get_height(node=node.right)
        ) + 1
        # ANOTHER IMPLEMENTATION FOR THIS:
        # if node:        
        #     if node.right and (node.left and node.is_thread is False):
        #         return max(
        #             LeftThreadedBinaryTree.get_height(node.left),
        #             LeftThreadedBinaryTree.get_height(node.right),
        #         ) + 1
        #     if node.right:
        #         return LeftThreadedBinaryTree.get_height(node.right) + 1
        #     if node.left and node.is_thread is False:
        #         return LeftThreadedBinaryTree.get_height(node.left) + 1
        # return 0
    
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
                if current.is_thread:
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
                self.root.is_thread = False
        elif deleting_node == deleting_node.parent.right:
            # If d is its parent's right child
            deleting_node.parent.right = replacing_node
            if replacing_node and deleting_node.is_thread and replacing_node.is_thread:
                replacing_node.left = deleting_node.left
        else:
            # If d is its parent's left child
            deleting_node.parent.left = replacing_node
            if replacing_node:
                if deleting_node.is_thread and replacing_node.is_thread:
                    replacing_node.left = deleting_node.left
            else:
                deleting_node.parent.left = deleting_node.left
                deleting_node.parent.is_thread = True
        
        # fix the pointer to parent
        if replacing_node:
            replacing_node.parent = deleting_node.parent

            

# # test client

# tree = RightThreadedBinaryTree()
# print(RightThreadedBinaryTree.get_height(tree.root))  # Test None node case, should be 0
# tree.insert(key=4, data="")
# tree.insert(key=1, data="")
# tree.insert(key=7, data="")
# tree.insert(key=3, data="")
# tree.insert(key=5, data="")
# tree.insert(key=8, data="")
# tree.insert(key=2, data="")
# # tree.insert(key=2.5, data="")
# tree.insert(key=6, data="")
# print(RightThreadedBinaryTree.get_height(tree.search(1)))
# print("Before deleting: ")
# tree.root.display_keys(tree)
# print(list(tree.inorder_traverse()))
# tree.delete(7)
# print("After deleting: ")
# tree.root.display_keys(tree)
# print(list(tree.preorder_traverse()))
# print(tree.search(3).right.key)
# print("-----------------------")
# 
# tree = LeftThreadedBinaryTree()
# tree.insert(key=4, data="")
# tree.insert(key=1, data="")
# tree.insert(key=7, data="")
# tree.insert(key=3, data="")
# tree.insert(key=5, data="")
# tree.insert(key=8, data="")
# tree.insert(key=2, data="")
# tree.insert(key=6, data="")
# # print("Before deleting: ")
# # tree.root.display_keys(tree)
# # print(list(tree.reverse_inorder_traverse()))

# tree.delete(4)
# print("After deleting: ")
# tree.root.display_keys(tree)
# print(list(tree.reverse_inorder_traverse()))
# print(tree.search(6).left.key)