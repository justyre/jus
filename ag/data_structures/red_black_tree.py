# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Red-black tree implementation (with only insertion deployed)."""

#####################
# Self-balancing binary search tree called Red Black Tree, where each node has 
# an extra bit interpreted as the color (red or black). The colors are used to 
# ensure that the tree remains balanced during insertions and deletions.
# 
# Properties of a red black tree:
# 1. Each node has a color, red or black.
# 2. The root of the tree is always black.
# 3. There are no two adjacent red nodes, ie a red node cannot have a red parent
#  or a red child.
# 4. Every simple path from a node to any of its descendant NIL nodes has the 
# same number of black nodes. (A NIL node aka a leaf is always black.)
#
# Black height := # black nodes on a path from the root to a leaf (not counting 
# the root). According to Property 3, each red node strictly requires black 
# children, black_height(root) >= height(root)/2.
#
# Then we introduce the following lemma: 
# Lemma: A subtree rooted at node v has >= 2^black_height(v) - 1 internal nodes.
# Proof by induction: The basis is when height(v) = 0, ie v is a leaf, and hence
#  black_height(v) = 0, and the subtree rooted at v has 2^0-1=0 nodes.
# The inductive hypothesis is: If node v1 w/height x (as the child) has 
# >= 2^bh(v1)-1 internal nodes, then node v2 w/height x+1 (as the parent) has 
# >= 2^bh(v2)-1 internal nodes.
# Actually, for any non-leaf node v1 (height>0), any of its child's black 
# height >= bh(v1)-1 (when the child is black, its bh is bh(v1)-1, coz itself 
# adds 1 to the bh count when computing bh of its parent v1; when the child is 
# red, its bh is just bh(v1)). Applying the hypothesis above, each child has at 
# least 2^(bh(v1)-1)-1 nodes, so v1's internal nodes >= 1 + 2*(2^(bh(v1)-1)-1)
# = 2^bh(v1) - 1. Child -> parent induction completed. QED
# Applying the lemma to the root node, we get: n >= 2^bh(root)-1 >= 2^(height/2)
# -1, ie height(root) <= 2 * log(n+1). So the height is O(log N).

# Every red black tree is a special case of a BST.

###########################
# ALGORITHM OF INSERTION

# We always try recoloring of a node first; if it does not work, then we go for 
# rotation.
# Let the inserting node be x.
# 1. Do a standard BST insertion of x. Assign x the red color.
# 2. If x is a root node, then change x's color to black.
# 3. If x is not a root node, check x's parent's color: if black, don't change; 
#  if red, then go on to the next step.
# 4. If x is not root AND x's parent is red, we check x's uncle: 
#  If x's uncle is red, we know from Property 3 that x's grandfather must be 
#  black. Then change its parent & 
#  its uncle to black, and change its grandfather to red. Repeat the process of 
#  Steps 2-4 for grandfather, treating grandfather as the new x.
# 5. If x's uncle is black, there are 4 possible cases:
#    a) Left Left Case (ie pa is left child of gran, x is left child of pa)
#    t1 to t5 are subtrees. p = pa of x, g = gran, u = uncle; r = red, b=black.
#    ((t1,xr,t2),pr,t3), gb, (t4,ub,t5) --> (t1,xr,t2), pb, (t3,gr,(t4,ub,t5))
#    This takes 2 steps: RightRotate(g), then swap colors of g & p.
#    b) Left Right Case (ie pa is left child of gran, x is right child of pa)
#    (t1,pr,(t2,xr,t3)), gb, (t4,ub,t5) --> ((t1,pr,t2),xr,t3), gb, (t4,ub,t5) 
#    --> (t1,pr,t2), xb, (t3,gr,(t4,ub,t5)).
#    This takes 3 steps: LeftRotate(p), RightRotate(g), swap colors of g & x.
#    c) Right Right Case (symmetric to Case a)
#    (t1,ub,t2), gb, (t3,pr,(t4,xr,t5)) --> ((t1,ub,t2),gr,t3), pb, (t4,xr,t5)
#    This takes one step: LeftRotate(g), then swap colors of g & p.
#    d) Right Left Case (symmetric to Case b)
#    (t1,ub,t2), gb, ((t3,xr,t4),pr,t5) --> (t1,ub,t2), gb, (t3,xr,(t4,pr,t5))
#    --> ((t1,ub,t2),gr,t3), xb, (t4,pr,t5).
#    This takes 3 steps: RightRotate(p), LeftRotate(g), swap colors of g & x.
##########################

RED = 'red'
BLACK = 'black'

class Leaf():
    """Leaf node. Not inherited from `IterMixin` class."""
    
    def __init__(self, color=BLACK):
        self.key = None
        self.color = color

    def isLeaf(self):
        """Check if a node is leaf node."""
        return True

class IterMixin:
    """A class that iterates over all its `__dict__` items (ie methods, global vars)."""
    
    def __iter__(self):
        """With this, we can iterate by `for attr, value in itermixin:`."""
        for attr, value in self.__dict__.items():
            yield attr, value

class Node(IterMixin):
    """Node. Inherited from `IterMixin` class."""
    
    def __init__(self, key, parent=None, left=None, right=None):
        self.key = key
        self.parent = parent
        self.left = left
        self.right = right

    def getGrandparent(self):
        """Get the grandparent of a node."""
        grandparent = None
        if self.parent is not None:
            grandparent = self.parent.parent
        return grandparent

    def getUncle(self):
        """Get the uncle of a node (ie the child of grandparent that is not parent)."""
        uncle = None
        if self.parent is not None and self.parent.parent is not None:
            if self.parent is self.getGrandparent().left:
                uncle = self.getGrandparent().right
            else:
                uncle = self.getGrandparent().left
        return uncle

class RedBlackNode(Node):
    """Node of a red-black tree that is not a leaf."""
    
    def __init__(self, key, color=RED, parent=None, left=Leaf(), right=Leaf()):
        self.key = key
        self.parent = parent
        self.left = left
        self.right = right
        self.color = color

    def isLeaf(self):
        """Check if a node is leaf node."""
        return False

class Tree:
    """A basic binary search tree."""
    
    def __init__(self, root=None, nodes=set()):
        self.root = root
        self.nodes = nodes  # set in Python is non-ordered and non-duplicated
        if root is not None:
            self.nodes.add(root)  # if root already exists in the set, do nothing
      
    def insertNode(self, next_node, node):
        """Insert node."""
        if node.key < next_node.key:
            if next_node.left is None:
                next_node.left = node
                node.parent = next_node
            else:
                self.insertNode(next_node.left, node)
            return
        if next_node.right is None:
            next_node.right = node
            node.parent = next_node
        else:
            self.insertNode(next_node.right, node)

    def addNode(self, node):
        """Add node to the set of nodes in the tree, and insert it into the tree."""
        self.nodes.add(node)
        self.insertNode(self.root, node)

class RedBlackTree(Tree):
    """Red-black tree. Inherited from `Tree` class."""
    
    def __init__(self, root=None, nodes=set()):
        self.root = root
        self.nodes = nodes
        if root is not None:
            self.nodes.add(root)
            self.root.color = BLACK

    def insertNode(self, next_node, node):
        """Insert node."""
        if node.key < next_node.key:
            if next_node.left.isLeaf():
                next_node.left = node
                node.parent = next_node
            else:
                self.insertNode(next_node.left, node)
            return
        if next_node.right.isLeaf():
            next_node.right = node
            node.parent = next_node
        else:
            self.insertNode(next_node.right, node)

    def rotateLeft(self, node):
        """Left rotation."""
        parent = node.parent
        right_child = node.right
        right_child_left = right_child.left

        parent.right = right_child
        right_child.parent = parent

        right_child.left = node
        node.parent = right_child

        node.right = right_child_left
        right_child_left.parent = node

        if node is self.root:
            self.root = right_child

    def rotateRight(self, node):
        """Right rotation."""
        parent = node.parent
        left_child = node.left
        left_child_right = left_child.right

        parent.left = left_child
        left_child.parent = parent

        left_child.left = node
        node.parent = left_child

        node.left = left_child_right
        left_child_right.parent = node

        if node is self.root:
            self.root = left_child


    def balance(self, node):
        """Adjust the structures and colors to retain red-black tree properties."""
        if node is not self.root:
            if node.parent is None:
                return
            if node.parent.color is BLACK:
                return
            if node.getGrandparent() is not None:
                grandparent = node.getGrandparent()
                uncle = node.getUncle()
                if uncle.color is RED:
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    grandparent.color = RED
                    self.balance(grandparent)
                    return
                elif node is node.parent.right and node.parent is grandparent.left:
                    self.rotateLeft(node.parent)
                    node = node.left
                elif node is node.parent.left and node.parent is grandparent.right:
                    self.rotateRight(node.parent)
                    node = node.right
                grandparent = node.getGrandparent()
                node.parent.color = BLACK
                grandparent.color = RED
                if node is node.parent.left:
                    self.rotateRight(grandparent)
                else:
                    self.rotateLeft(grandparent)
        self.root.color = BLACK

    def addNode(self, node):
        """Add node to the set of nodes in the tree, and insert it into the tree."""
        self.nodes.add(node)
        self.insertNode(self.root, node)
        self.balance(node)



# Driver code

node1 = RedBlackNode(13)
tree = RedBlackTree(node1)
values = [2, 15, 28, 5, 1, 30, 32]

for val in values:
    new_node = RedBlackNode(val)
    tree.addNode(new_node)


print(f"Root node is: {tree.root.key}")
i = 1
for node in tree.nodes:
    print(f'Node {i}:')
    print(f'Address: {node}')
    for key, values in node:
        print(f'{key}: {values}')
    print('------------------------')
    i += 1