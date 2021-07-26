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


############################
# PYTHON IMPLEMENTATION

# generic tree node class
class TreeNode:
    def __init__(self, val) -> None:
        self.val = val
        self.left = None
        self.right = None
        self.parent = None
        self.color = 'R'
        
# Red black tree class which supports the insert operation
class RedBlackTree:
    
    # search a given `key` in `root`
    def search(self, root, key):
        if root is None or root.val == key:
            return root
        if key < root.val:
            return self.search(root.left, key)
        return self.search(root.right, key)
    
    # insertion
    def insert(self, root, key):
        
        # step 1: perform standard BST insertion
        if not root:
            new_treenode = TreeNode(key)
            new_treenode.color = 'B'
            return new_treenode
        elif key < root.val:
            root.left = self.insert(root.left, key)
            root.left.parent = root            
        # we assume that we do not insert a key that already exists in `root`
        else:
            root.right = self.insert(root.right, key)
            root.right.parent = root
    
        if root.parent is not None and root.parent.color == 'R':
            # check which side parent is on of gran, so we can find uncle
            if root.parent.right == root:
                if root.parent.left is None or root.parent.left.color == 'R':
                    # pa is red, uncle is red
                    root.parent.color = 'B'
                    root.parent.left.color = 'B'
                    if root.parent.parent is not None:
                        root.parent.parent.color = 'R'
                    pass
            else:
                if root.parent.right is None or root.parent.right.color == 'R':
                    pass
                    
                    
        
        
        
    # left rotate of red black tree. eg:
    #    t1, z, (t2,y,(t3,x,t4)) --> (t1,z,t2), y, (t3,x,t4)
    #    This takes one step: LeftRotate(z).
    def left_rotate(self, z):
        
        y = z.right
        t2 = y.left
        
        # perform rotation
        y.left = z
        z.right = t2
        z.parent = y  # parent resetting is also important
        if t2:
            t2.parent = z
        
        # return the new root
        return y
    
    # right rotate of red black tree. eg:
    #    ((t1,x,t2),y,t3), z, t4 --> (t1,x,t2), y, (t3,z,t4)
    #    This takes one step: RightRotate(z).
    def right_rotate(self, z):
        y = z.left
        t3 = y.right
        
        # perform rotation
        y.right = z
        z.left = t3
        z.parent = y
        if t3:
            t3.parent = z
        
        # return the new root
        return y