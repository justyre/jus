# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Red-Black Tree."""

import dataclasses
import enum
from typing import Any, Optional, Union

from forest import metrics
from forest import tree_exceptions
from forest.binary_trees import binary_tree


class Color(enum.Enum):
    """Color definition for Red-Black Tree."""
    
    RED = enum.auto()
    BLACK = enum.auto()
    
@dataclasses.dataclass
class Leaf():
    """Definition of a leaf node in Red-Black Tree whose color is always black."""

    # Note: Leaf is not inherited from b_t.Node, since we want empty() method of 
    # b_t.BinaryTree to work for red-black trees, too
    color = Color.BLACK
    
@dataclasses.dataclass
class Node(binary_tree.Node):
    """Definition of a Red-Black Tree non-leaf node."""
    
    left: Union["Node", Leaf] = Leaf()
    right: Union["Node", Leaf] = Leaf()
    parent: Union["Node", Leaf] = Leaf()
    color: Color = Color.RED
    
    def display_keys(self, space: str = '\t', level: int = 0) -> None:
        """Display all the keys in a Node horizontally for clear visualization.
        
        For colored trees, also display each node's color.
        """
        if isinstance(self, Leaf):
            print(space * level + '∅')
            return
        
        # if the node has two NIL children, print node.key and node.color
        if isinstance(self.left, Leaf) and isinstance(self.right, Leaf):
            print(space * level, str(self.key), str(self.color)[6])
            return
        
        # if the node has children, show right subtree up, left subtree down
        Node.display_keys(self.right, space, level + 1)
        print(space * level, str(self.key), str(self.color)[6])
        Node.display_keys(self.left, space, level + 1)
    
class RBTree(binary_tree.BinaryTree):
    """Red-Black Tree.
    
    Attributes
    ----------
    root: `Union[Node, Leaf]`
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
    get_height(node: `Union[Node, Leaf]`)
        Return the height of the given node.
        
    Traversal Functions
    inorder_traverse()
        Reverse in-order traversal (LDR).
    preorder_traverse()
        Pre-order traversal (DLR).
    postorder_traverse()
        Post-order traversal (LRD).
        
    Examples
    --------
    >>> from forest.binary_trees import red_black_tree
    >>> tree = red_black_tree.RBTree()
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

    # Red-Black Tree properties:
    # 1. Each node is red or black.
    # 2. Root is black.
    # 3. Each leaf (aka NIL) is black.
    # 4. If a node is red, then both of its children are black.
    # 5. For any node, all the simple paths from itself to a descendent leaf contains 
    #    the same number of black nodes.
    # 
    # By convention, we use NIL to denote leaves for the RBT, and they are always black.
    # 
    # Black height = # black nodes from a node to the leaves, excluding itself if it's 
    # black. All leaf nodes (ie NILs) have black height zero.
    # 
    # A red-black tree is a self-balancing BST and as a height of at most 2 * log(N+1) 
    # (For proof, cf. CLRS "Introduction to Algorithms" Lemma 13.1). Hence, for all the 
    # methods in this class (insert, search, delete, leftmost, rightmost, predecessor, 
    # successor), both the average and worst case time complexities are O(log N).
    #
    # Although maintaining RBT properties is complicated, its self-balancing ability 
    # makes RBTs perform better than ordinary BSTs.
    
    def __init__(self, registry: Optional[metrics.MetricRegistry] = None) -> None:
        binary_tree.BinaryTree.__init__(self)
        self._NIL: Leaf = Leaf()
        self.root: Union[Node, Leaf] = self._NIL
        
        self._metrics_enabled = True if registry else False
        if self._metrics_enabled:
            self._rotate_counter = metrics.Counter()
            self._height_histogram = metrics.Histogram()
            registry.register(name="rbt.rotate", metric=self._rotate_counter)
            registry.register(name="rbt.height", metric=self._height_histogram)    
    
    # Override
    def search(self, key: Any) -> Optional[Node]:
        """Look for a node by a given key.

        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.search`.
        """
        current: Optional[Node] = self.root
        while isinstance(current, Node):
            # So c is a Node obj, not a Leaf obj
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                return current
        # if nothing matches key, the node does not exist in the tree.
        # Note: If the tree is empty, ie self.root==Leaf(), we return None too
        return None
    
    # Override
    def insert(self, key: Any, data: Any) -> None:
        """Insert a (key, data) pair into the red-black tree.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.insert`.
        """
        # Color the new node red
        new_node = Node(key=key, data=data, color=Color.RED)
        parent: Union[Node, Leaf] = self._NIL
        current: Union[Node, Leaf] = self.root
        while isinstance(current, Node):
            parent = current
            if new_node.key < current.key:
                current = current.left
            elif new_node.key > current.key:
                current = current.right
            else:
                raise tree_exceptions.DuplicateKeyError(key=new_node.key)
        new_node.parent = parent
        if isinstance(parent, Leaf):
            # if the tree is empty (ie parent is a Leaf), set the new node to be root, 
            # which must be black as per Property #2
            new_node.color = Color.BLACK
            self.root = new_node
        else:
            if new_node.key < parent.key:
                parent.left = new_node
            else:
                parent.right = new_node
            # After insertion, fix the broken RBT properties
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
        # if root is not None and the node to be deleted is not None
        if (deleting_node := self.search(key=key)) and isinstance(deleting_node, Node):
            original_color = deleting_node.color
            
            # Case 1: deleting_node has no child, then replace deleting_node with None.
            # Case 2a: only one right child, then replace deleting_node with the child.
            # Together, these two cases can be seen as replacing with its right child.
            if isinstance(deleting_node.left, Leaf):
                replacing_node = deleting_node.right
                self._transplant(
                    deleting_node=deleting_node, replacing_node=replacing_node
                )
                # Fixup
                # Note: If we delete a red childless node, we replace it with a black 
                # NIL (since d.r=NIL), all RBT properties preserved. If we delete a 
                # black childless node, "equal black height" is broken.
                if original_color == Color.BLACK and isinstance(replacing_node, Node):
                    self._delete_fixup(fixing_node=replacing_node)
                                
            # Case 2b: deleting_node has only one left child
            elif isinstance(deleting_node.right, Leaf):
                replacing_node = deleting_node.left
                self._transplant(
                    deleting_node=deleting_node, replacing_node=replacing_node
                )
                # Fixup
                # Note: If d is red, by RBT property, it must have TWO black children. 
                # So in this Case 2b, d can only be black.
                # And for a black node, due to "equal black height", it cannot have only
                # one black child, either. So r=d.l must be red.
                if original_color == Color.BLACK and isinstance(replacing_node, Node):
                    self._delete_fixup(fixing_node=replacing_node)
            
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
                original_color = replacing_node.color
                replacing_right = replacing_node.right
                # Case 3c. 
                # Note: by definition of replacing_node, it cannot have a left child.
                if replacing_node.parent == deleting_node:
                    if isinstance(replacing_node.right, Node):
                        replacing_node.right.parent = replacing_node
                else:
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
                replacing_node.color = deleting_node.color
                # Fixup. Note that in this case, both d and r can be black or red.
                if original_color == Color.BLACK and isinstance(replacing_right, Node):
                    self._delete_fixup(fixing_node=replacing_right)
        
        if self._metrics_enabled:
            self._height_histogram.update(value=self.get_height(self.root))            

    # Note: @staticmethod ensures that `self` is not passed implicitly as get_height()'s
    # first argument. Compare with insert/search/delete, who all have `self` as 1st arg.
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
        while isinstance(current_node.left, Node):
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
        while isinstance(current_node.right, Node):
            current_node = current_node.right
        return current_node
    
    # Override
    @staticmethod
    def get_predecessor(node: Node) -> Union[Node, Leaf]:
        """Return the predecessor in the in-order order.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.get_predecessor`.
        """
        # Case 1: left child is not a Leaf
        if isinstance(node.left, Node):
            return RBTree.get_rightmost(node=node.left)
        # Case 2: left child is a Leaf
        parent = node.parent
        # Move up until node is the right child, and return its parent
        while isinstance(parent, Node) and (node == parent.left):
            node = parent
            parent = parent.parent
        return parent
    
    # Override
    @staticmethod
    def get_successor(node: Node) -> Union[Node, Leaf]:
        """Return the successor in the in-order order.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.get_successor`.
        """
        # Case 1: right child is not a Leaf
        if isinstance(node.right, Node):
            return RBTree.get_leftmost(node=node.right)
        # Case 2: right child is a Leaf
        parent = node.parent
        # Move up until node is the left child, and return its parent
        while isinstance(parent, Node) and (node == parent.right):
            node = parent
            parent = parent.parent
        return parent

    # Override
    @staticmethod
    def get_height(node: Union[Node, Leaf]) -> int:
        """Get the height of the given subtree.
        
        See Also
        --------
        :py:meth:`forest.binary_trees.binary_tree.BinaryTree.get_height`.
        """
        if isinstance(node, Leaf):
            return 0
        if isinstance(node.left, Leaf) and isinstance(node.right, Leaf):
            return 0
        return max(
            RBTree.get_height(node=node.left), RBTree.get_height(node=node.right)
        ) + 1

    def inorder_traverse(self) -> binary_tree.Pairs:
        """Perform In-Order traversal.
        
        In-order traversal traverses a tree by the order:
        left subtree, current node, right subtree (LDR)
        
        Yields
        ------
        `Pairs`
            The next (key, data) pair in the in-order traversal.
        
        Examples
        --------
        >>> from forest.binary_trees import red_black_tree
        >>> tree = red_black_tree.RBTree()
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
        >>> [item for item in tree.preorder_traverse()]
        [(1, '1'), (4, '4'), (7, '7'), (11, '11'), (15, '15'), (20, '20'),
        (22, '22'), (23, '23'), (24, '24'), (30, '30'), (34, '34')]
        """
        return self._inorder_traverse(node=self.root)

    def preorder_traverse(self) -> binary_tree.Pairs:
        """Perform Pre-Order traversal.
        
        Pre-order traversal traverses a tree by the order:
        current node, left subtree, right subtree (DLR)
        
        Yields
        ------
        `Pairs`
            The next (key, data) pair in the pre-order traversal.
            
        Examples
        --------
        >>> from forest.binary_trees import red_black_tree
        >>> tree = red_black_tree.RBTree()
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
        >>> [item for item in tree.preorder_traverse()]
        [(20, "20"), (7, "7"), (4, "4"), (1, "1"), (11, "11"), (15, "15"),
        (23, "23"), (22, "22"), (30, "30"), (24, "24"), (34, "34")]
        """
        return self._preorder_traverse(node=self.root)

    def postorder_traverse(self) -> binary_tree.Pairs:
        """Perform Post-Order traversal.
        
        Post-order traversal traverses a tree by the order:
        left subtree, right subtree, current node (LRD)
        
        Yields
        ------
        `Pairs`
            The next (key, data) pair in the post-order traversal.

        Examples
        --------
        >>> from forest.binary_trees import red_black_tree
        >>> tree = red_black_tree.RBTree()
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
        >>> [item for item in tree.postorder_traverse()]
        [(1, "1"), (4, "4"), (15, "15"), (11, "11"), (7, "7"), (22, "22"),
        (24, "24"), (34, "34"), (30, "30"), (23, "23"), (20, "20")]
        """
        return self._postorder_traverse(node=self.root)
    
    def _left_rotate(self, node_x: Node) -> None:
        # Left rotate node_x down and node_x.right up a level as the new subtree root.
        node_x_right = node_x.right
        if isinstance(node_x_right, Leaf):
            raise RuntimeError("Invalid left rotate: node_x.right cannot be a Leaf")
        
        # Turn nxr.l to nx.r
        node_x.right = node_x_right.left
        if isinstance(node_x_right.left, Node):
            node_x_right.left.parent = node_x
            # If nxr.l was a NIL, there is no need to set its parent (NILs have no dads)
        node_x_right.parent = node_x.parent
        
        # We need to decide where to hang nxr, which depends on the relation between 
        # nx and nx.pa: If nx.pa was a Leaf, nxr gets to be the new root. If nx was the 
        # left child of nx.pa, nxr should be nx.pa's new left child. Same if right child
        if isinstance(node_x.parent, Leaf):
            # If nx.pa was a Leaf, nxr is the new root
            self.root = node_x_right
        elif node_x == node_x.parent.left:
            node_x.parent.left = node_x_right
        else:
            node_x.parent.right = node_x_right
            
        # Now hang nx as nxr.l
        node_x_right.left = node_x
        node_x.parent = node_x_right
        
        if self._metrics_enabled:
            self._rotate_counter.increase()
    
    def _right_rotate(self, node_x: Node) -> None:
        # Right rotate node_x down and node_x.left up a level as the new subtree root.
        node_x_left = node_x.left
        if isinstance(node_x_left, Leaf):
            raise RuntimeError("Invalid right rotate: node_x.left cannot be a Leaf")
        
        # Turn nxl.r to nx.l
        node_x.left = node_x_left.right
        if isinstance(node_x_left.right, Node):
            node_x_left.right.parent = node_x
        node_x_left.parent = node_x.parent
        
        if isinstance(node_x.parent, Leaf):
            self.root = node_x_left
        elif node_x == node_x.parent.left:
            node_x.parent.left = node_x_left
        else:
            node_x.parent.right = node_x_left
        
        # Now hang nx as nxl.r
        node_x_left.right = node_x
        node_x.parent = node_x_left
        
        if self._metrics_enabled:
            self._rotate_counter.increase()       
        
    def _insert_fixup(self, fixing_node: Node) -> None:
        # Fix a broken RBT to satisfy the RBT properties again. 
        # fixing_node is the newly inserted node.
        # Only Properties #[2,4] can be violated after an insertion. Regarding #2, 
        # we only need to color the root black at the end of function. Regarding #4, 
        # we break down into 6 cases. 
        # (Note that if fn.pa is black, there is nothing to fix up, everything is fine; 
        # so only consider fn.pa is red. Since it was RBT before insertion, fn.grandpa,
        # denoted fn.pp from now on, must be black.)
        while fixing_node.parent.color == Color.RED:
            if fixing_node.parent == fixing_node.parent.parent.left:
                # fn is red, fn.pa is left child of fn.pp
                parent_sibling = fixing_node.parent.parent.right
                if parent_sibling.color == Color.RED:
                    # Case 1: s is red
                    fixing_node.parent.color = Color.BLACK
                    parent_sibling.color = Color.BLACK
                    fixing_node.parent.parent.color = Color.RED
                    fixing_node = fixing_node.parent.parent
                else:
                    if fixing_node == fixing_node.parent.right:
                        # Case 2: s is black, fn is right child of fn.pa.
                        # Then we transform it into Case 3
                        fixing_node = fixing_node.parent
                        self._left_rotate(fixing_node)
                    # Case 3: s is black, fn is left child of fn.pa.
                    fixing_node.parent.color = Color.BLACK
                    fixing_node.parent.parent.color = Color.RED
                    # Why right rotate? If not, when s is NIL (black), RBT Property #5 
                    # (equal black height) will be violated, 
                    # since bh(fn.pp to fn)=bh(fn.pp to s)+1.
                    self._right_rotate(fixing_node.parent.parent)
            else:
                # fn is red, fn.pa is right child of fn.pp
                parent_sibling = fixing_node.parent.parent.left
                if parent_sibling.color == Color.RED:
                    # Case 4: s is red (symmetical to Case 1)
                    fixing_node.parent.color = Color.BLACK
                    parent_sibling.color = Color.BLACK
                    fixing_node.parent.parent.color = Color.RED
                    fixing_node = fixing_node.parent.parent
                else:
                    if fixing_node == fixing_node.parent.left:
                        # Case 5: s is black, fn is left child of fn.pa.
                        # This is symmetrical to Case 2
                        fixing_node = fixing_node.parent
                        self._right_rotate(fixing_node)
                    # Case 6: s is black, fn is right child of fn.pa
                    fixing_node.parent.color = Color.BLACK
                    fixing_node.parent.parent.color = Color.RED
                    self._left_rotate(fixing_node.parent.parent)
        
        self.root.color = Color.BLACK

    def _delete_fixup(self, fixing_node: Union[Node, Leaf]) -> None:
        # Fix a broken RBT to satisfy the RBT properties again. 
        # fixing_node is usually the replacing node, except for when d has two children,
        # where fn is the node that takes r(ie the leftmost node)'s position, ie r_r
        while (fixing_node is not self.root) and (fixing_node.color == Color.BLACK):
            # If the root needs fixing, set it black.
            if fixing_node == fixing_node.parent.left:
                sibling = fixing_node.parent.right
                if isinstance(sibling, Leaf):
                    break
                
                # Case 1: fn is the left child, s is red
                if sibling.color == Color.RED:
                    sibling.color = Color.BLACK
                    fixing_node.parent.color = Color.RED
                    self._left_rotate(fixing_node.parent)
                    sibling = fixing_node.parent.right                
                
                # Case 2: fn is the left child, s is black, s's children are black
                elif sibling.color == Color.BLACK and sibling.left.color == Color.BLACK and sibling.right.color == Color.BLACK:
                    sibling.color = Color.RED
                    fixing_node = fixing_node.parent
                
                else:
                    if sibling.right.color == Color.BLACK:
                        # Case 3: fn is the left child, s is black, and s's left child 
                        # is red, s's right child is black. (double black kids in Case2)
                        sibling.left.color = Color.BLACK
                        sibling.color = Color.RED
                        self._right_rotate(sibling)
                    
                    # Case 4: fn is the left child, s is black, (s.l, s.r) is BR.
                    # Note: (s.l, s.r) cannot be RR, for an example cannot be devised.
                    sibling.color = fixing_node.parent.color
                    fixing_node.parent.color = Color.BLACK
                    sibling.right.color = Color.BLACK
                    self._left_rotate(fixing_node.parent)
                    # Once we are here, all the violations against RBT properties have 
                    # been fixed. So move to the root to terminate the loop.
                    fixing_node = self.root
            
            else:
                sibling = fixing_node.parent.left
                if isinstance(sibling, Leaf):
                    break
                
                # Case 5: fn is the right child, s is red (Symm to Case 1)
                if sibling.color == Color.RED:
                    sibling.color = Color.BLACK
                    fixing_node.parent.color = Color.RED
                    self._right_rotate(fixing_node.parent)
                    sibling = fixing_node.parent.left                
                
                # Case 6: fn is the right child, s is black, s's children are black
                elif sibling.color == Color.BLACK and sibling.left.color == Color.BLACK and sibling.right.color == Color.BLACK:
                    sibling.color = Color.RED
                    fixing_node = fixing_node.parent
                
                else:
                    if sibling.left.color == Color.BLACK:
                        # Case 7: fn is the right child, s is black, and (s.l, s.r) is 
                        # BR. (double black kids in Case 6)
                        sibling.right.color = Color.BLACK
                        sibling.color = Color.RED
                        self._left_rotate(sibling)
                    
                    # Case 8: fn is the right child, s is black, (s.l, s.r) is RB.
                    # Note: (s.l, s.r) cannot be RR, for an example cannot be devised.
                    sibling.color = fixing_node.parent.color
                    fixing_node.parent.color = Color.BLACK
                    sibling.left.color = Color.BLACK
                    self._right_rotate(fixing_node.parent)
                    # Once we are here, all the violations against RBT properties have 
                    # been fixed. So move to the root to terminate the loop.
                    fixing_node = self.root
            
        # Set root to black
        fixing_node.color = Color.BLACK

    def _transplant(
        self, deleting_node: Node, replacing_node: Union[Node, Leaf]
    ) -> None:
        # An internal function (thus not requiring a docstring & is defined with 
        # a leading underscore) to replace the subtree rooted at `deleting_node` with 
        # the subtree rooted at `replacing_node`.
        # Note: By definition, this function has established all connections ABOVE 
        # `old d/new r` node, ie it has already set `r.parent = d.parent`. But this 
        # function does not consider whether putting r in d's place preserves BST.
        
        if isinstance(deleting_node.parent, Leaf):
            self.root = replacing_node
        elif deleting_node == deleting_node.parent.left:
            deleting_node.parent.left = replacing_node
        else:
            deleting_node.parent.right = replacing_node
        # if replacing_node is not None, point it to the orig deleting_node's parent 
        if isinstance(replacing_node, Node):
            replacing_node.parent = deleting_node.parent
    
    def _inorder_traverse(self, node: Union[Node, Leaf]) -> binary_tree.Pairs:
        if isinstance(node, Node):
            yield from self._inorder_traverse(node.left)
            yield (node.key, node.data)
            yield from self._inorder_traverse(node.right)

    def _preorder_traverse(self, node: Union[Node, Leaf]) -> binary_tree.Pairs:
        if isinstance(node, Node):
            yield (node.key, node.data)
            yield from self._preorder_traverse(node.left)
            yield from self._preorder_traverse(node.right)

    def _postorder_traverse(self, node: Union[Node, Leaf]) -> binary_tree.Pairs:
        if isinstance(node, Node):
            yield from self._postorder_traverse(node.left)
            yield from self._postorder_traverse(node.right)
            yield (node.key, node.data)
