"""Implementation of AVL tree, a kind of self-balancing BST tree."""

#############################
# Self-balancing binary tree that remains balanced after each insertion/ 
# deletion. We discuss the AVL trees here, where self-balancing is achieved 
# by tracking the `balance factor` (:= height of the left subtree - height of 
# the right subtree) for each node, & rotating unbalanced subtrees along 
# the path of insertion/deletion to balance them.
# 
# In a balanced binary search tree, the balance factor of any node is one of 
# [-1, 0, 1]. When we perform an insertion, the balance factor of some nodes 
# along the path of insertion may change to 2 or -2. Those nodes can be 
# `rotated` one-by-one to bring their balance factors back to [-1, 0, 1].
# 
# Time complexity: 
# For one insertion, we need O(log N) (ie order of height) time to find the 
# place to insert the node rotation, and then we might have to go O(log N)
# levels to find the unbalanced node, and do a rotation that takes const time 
# O(1) to balance that rode. So the total time for insertion is O(log N). 
# This is far more efficient than 
# creating a balanced binary tree from scratch, which requires O(N).
#
# For one deletion, we need O(log N) to find the node to be deleted, and then 
# spend O(log N) traveling up the tree to find the first place where imbalance 
# occurs. Having found that, we do a rotation that may or may not keep the 
# height balanced. If it does not restore the height balance, we will have to 
# continue traveling up and may once again perform a rotation... so at most, 
# we may need to do O(log N) rotations, with each rotation taking O(1). Thus, 
# the total time for deletion is O(log N).
#
# Comparison w/Red Black Tree:
# If the application involves frequent insertions/deletions, use Red Black Tree.
# Otherwise, if search is the more frequent operation, AVL is preferred.
# AVL trees are more balanced than Red Black Trees.

###########################
# ALGORITHM OF INSERTION

# Let the newly inserted node be w.
# 1. Perform standard BST insertion for w.
# 2. Starting from w, travel up and find the FIRST UNBALANCED node z. 
#    Let y be the child of z that is on the path from w to z, and 
#    let x be the grandchild of z that is on the path w -> z.
# 3. Rebalance the tree by doing appropriate rotations on the subtree rooted at 
#    z. There are 4 possible cases we need to handle, as shown below. In all of 
#    these cases, we only need to rebalance the subtree rooted at z, and then 
#    the whole big tree becomes balanced, coz the height of subtree after proper
#     rotations equals the height of it before the rotations.
#    a) Left Left Case (ie y is left child of z, x is left child of y)
#    t1 to t4 are subtrees. 
#    ((t1,x,t2),y,t3), z, t4 --> (t1,x,t2), y, (t3,z,t4)
#    This takes one step: RightRotate(z).
#    b) Left Right Case (ie y is left child of z, x is right child of y)
#    (t1,y,(t2,x,t3)), z, t4 --> ((t1,y,t2),x,t3), z, t4 
#    --> (t1,y,t2), x, (t3,z,t4).
#    This takes two steps: LeftRotate(y), RightRotate(z).
#    c) Right Right Case (symmetric to Case a)
#    t1, z, (t2,y,(t3,x,t4)) --> (t1,z,t2), y, (t3,x,t4)
#    This takes one step: LeftRotate(z).
#    d) Right Left Case (symmetric to Case b)
#    t1, z, ((t2,x,t3),y,t4) --> t1, z, (t2,x,(t3,y,t4))
#    --> (t1,z,t2), x, (t3,y,t4).
#    This takes two steps: RightRotate(y), LeftRotate(z).

###########################
# ALGORITHM OF DELETION

# Let the node to be deleted be w.
# 1. Perform standard BST insertion for w.
# 2. Starting from w, travel up and find the FIRST UNBALANCED node z. 
#    Let y be the larger height child of z (y is proven to be unique), and 
#    let x be the larger height child of y (x can be ambiguous, as both 
#    children of y may have the same height since y is balanced).
# 3. Rebalance the tree by doing appropriate rotations on the subtree rooted at 
#    z. There are 4 possible cases we need to handle, as shown below. 
#    NOTE: Unlike insertion, fixing node z won't necessarily fix the whole AVL 
#    tree. After fixing z, we may have to fix ancestors of z as well, ie
#    we may have to trace the path until we reach the root.
#    a) Left Left Case (ie y is left child of z, x is left child of y)
#    t1 to t4 are subtrees. 
#    ((t1,x,t2),y,t3), z, t4 --> (t1,x,t2), y, (t3,z,t4)
#    This takes one step: RightRotate(z).
#    b) Left Right Case (ie y is left child of z, x is right child of y)
#    (t1,y,(t2,x,t3)), z, t4 --> ((t1,y,t2),x,t3), z, t4 
#    --> (t1,y,t2), x, (t3,z,t4).
#    This takes two steps: LeftRotate(y), RightRotate(z).
#    c) Right Right Case (symmetric to Case a)
#    t1, z, (t2,y,(t3,x,t4)) --> (t1,z,t2), y, (t3,x,t4)
#    This takes one step: LeftRotate(z).
#    d) Right Left Case (symmetric to Case b)
#    t1, z, ((t2,x,t3),y,t4) --> t1, z, (t2,x,(t3,y,t4))
#    --> (t1,z,t2), x, (t3,y,t4).
#    This takes two steps: RightRotate(y), LeftRotate(z).

############################
# PYTHON IMPLEMENTATION

class TreeNode:
    """Tree node."""
    
    def __init__(self, val) -> None:
        self.val = val
        self.left = None
        self.right = None
        self.height = 1
        
class AVLTree:
    """AVL tree class which supports the insert & delete operation."""

    def insert(self, root, key):
        """Recursively insert a node with given `key` into tree rooted with `root`."""
        # returns new `root` of the modified tree. (`root` is of class TreeNode)
        # step 1: perform standard BST insertion
        if not root:
            return TreeNode(key)
        elif key < root.val:
            root.left = self.insert(root.left, key)
        # we assume that we do not insert a key that already exists in `root`
        else:
            root.right = self.insert(root.right, key)
            
        # step 2: update the height of the current (ie ancestor) node
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        
        # step 3: get the balance factor
        balance_factor = self.balance_factor(root)
        
        # step 4: if the node is unbalanced, try out the 4 cases
        # case a: left left
        if balance_factor > 1 and key < root.left.val:
            return self.right_rotate(root)
        # case b: left right
        if balance_factor > 1 and key > root.left.val:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        # case c； right right
        if balance_factor < -1 and key > root.right.val:
            return self.left_rotate(root)
        # case d: right left
        if balance_factor < -1 and key < root.right.val:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root
    
    def delete(self, root, key):
        """Recursively delete a node with given `key` into tree rooted with `root`."""
        # returns new `root` of the modified tree.
        # step 1: perform standard BST deletion
        # if root is None, return None
        if not root:
            return root
        elif key < root.val:
            root.left = self.delete(root.left, key)
        elif key > root.val:
            root.right = self.delete(root.right, key)
        # note: unlike insert(), it is totally possible that we may delete 
        # the root node
        else:
            # if root has no left child, return its right child
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            # otherwise, both root's left & right children are non-None
            # since prev if & elif have returned, we don't need `else` here
            # NOTE: the next 3 lines do the following: if we are deleting a 
            # node `root` in the orig tree, first we find the leftmost grand-
            # child `temp` (which is also the minimum) of subtree `root.right`. 
            # Now we have key(root.left) < key(root) < key(temp) < key(root.
            # right except for temp). So to ensure the subtree is still a BST, 
            # we can replace root w/temp, delete temp from root.right, and point
            # the one-node-deleted root.right as the new root's right child.
            temp = self.min_value_node(root.right)
            root.val = temp.val
            root.right = self.delete(root.right, temp.val)
            
        # step 2: update the height of the current (ie ancestor) node
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        
        # step 3: get the balance factor
        balance_factor = self.balance_factor(root)
        
        # step 4: if the node is unbalanced, try out the 4 cases
        # case a: left left (ie left child of z has greater height, & 
        # left grandchild of z has greater or equal height)
        if balance_factor > 1 and self.balance_factor(root.left) >= 0:
            return self.right_rotate(root)
        # case b: left right
        if balance_factor > 1 and self.balance_factor(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        # case c； right right
        if balance_factor < -1 and self.balance_factor(root.right) <= 0:
            return self.left_rotate(root)
        # case d: right left
        if balance_factor < -1 and self.balance_factor(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root        
        
    def height(self, root):
        """Return the height of node `root`, considering the `root is None` case."""
        return root.height if root else 0
    
    def balance_factor(self, root):
        """Get the balance factor of `root`."""
        return self.height(root.left) - self.height(root.right) if root else 0
      
    def min_value_node(self, root):
        """Get the min value node of the subtree rooted with `root`."""
        # returning the leftmost leaf or (when root is None) None.
        # Since the result is the leftmost grandchild, it 
        # must be the minimum of all keys in subtree `root` (remember that 
        # `root` is a BST).
        if root is None or root.left is None:
            return root
        return self.min_value_node(root.left)
    
    def left_rotate(self, z):
        """Left rotation."""
        #    t1, z, (t2,y,(t3,x,t4)) --> (t1,z,t2), y, (t3,x,t4)
        #    This takes one step: LeftRotate(z).
        y = z.right
        t2 = y.left
        
        # perform rotation
        y.left = z
        z.right = t2
        
        # update heights
        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        
        # return the new root
        return y
    
    def right_rotate(self, z):
        """Right rotation."""
        #    ((t1,x,t2),y,t3), z, t4 --> (t1,x,t2), y, (t3,z,t4)
        #    This takes one step: RightRotate(z).
        y = z.left
        t3 = y.right
        
        # perform rotation
        y.right = z
        z.left = t3
        
        # update heights
        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        
        # return the new root
        return y
    
    def preorder_traversal(self, root):
        """Preorder traversal: (key, left, right)."""
        if not root:
            return
        print("{0} ".format(root.val), end="")
        self.preorder_traversal(root.left)
        self.preorder_traversal(root.right)

    def display_keys(self, root, space='\t', level=0):
        """Display the keys of a `TreeNode` object in a horizontal hierarchy."""
        # debugcode next line
        # print(root.val if root else None, level)
        # if the node is empty, print the empty set symbol
        if root is None:
            print(space * level + '∅')
            return
        
        # if the node is a leaf, print node.key
        if root.left is None and root.right is None:
            print(space * level + str(root.val))
            return
        
        # if the node has children, show right subtree up, left subtree down
        self.display_keys(root.right, space, level + 1)
        print(space * level + str(root.val))
        self.display_keys(root.left, space, level + 1)


######################
# Driver code

myTree = AVLTree()
root = None
# nums = [10, 20, 30, 40, 50, 25]
nums = [9, 5, 10, 0, 6, 11, -1, 1, 2]
for num in nums:
    root = myTree.insert(root, num)

# show the traversal and tree structure 
print("Preorder traversal of the constructed AVL tree is:")
myTree.preorder_traversal(root)
print("\nBefore deletion: ")
myTree.display_keys(root)

# delete & show
key = 9
root = myTree.delete(root, key)
print("Preorder traversal after deletion is:")
myTree.preorder_traversal(root)
print("\nAfter deletion: ")
myTree.display_keys(root)