# This code is contributed by PranchalK

"""Another AVL tree implementation with inversion count incorporated."""

# An AVL Tree based Python program to
# count inversion in an array

from typing import Any, List, Optional

 
class Node:
    """New Node."""

    # Allocates a new
    # Node with the given key and NULL left
    # and right pointers.
    def __init__(self, key: Any):
        self.key: Any = key
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.height: int = 0
        self.size: int = 1
        

def display_keys(self: Node, space: str = '\t', level: int = 0) -> None:
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
    display_keys(self.right, space, level + 1)
    print(space * level, str(self.key), str(self.height))
    display_keys(self.left, space, level + 1)
        
def height(N: Optional[Node]) -> int:
    """Get the height of the tree rooted with N."""
    if N is None:
        return 0
    return N.height

def size(N: Optional[Node]) -> int:
    """Get the size of the tree rooted with N."""
    if N is None:
        return 0
    return N.size

def balance_factor(N: Optional[Node]) -> int:
    """Get Balance factor of Node N."""
    if N is None:
        return 0
    return height(N.left) - height(N.right)

def right_rotate(y: Node) -> Node:
    """Right rotate a subtree rooted with y."""
    x = y.left
    T2 = x.right
 
    # Perform rotation
    x.right = y
    y.left = T2
 
    # Update heights
    y.height = max(height(y.left),
                   height(y.right)) + 1
    x.height = max(height(x.left),
                   height(x.right)) + 1
 
    # Update sizes
    y.size = size(y.left) + size(y.right) + 1
    x.size = size(x.left) + size(x.right) + 1
 
    # Return new root
    return x

def left_rotate(x: Node) -> Node:
    """Left rotate a subtree rooted with x."""
    y = x.right
    T2 = y.left
 
    # Perform rotation
    y.left = x
    x.right = T2
 
    # Update heights
    x.height = max(height(x.left),
                   height(x.right)) + 1
    y.height = max(height(y.left),
                   height(y.right)) + 1
 
    # Update sizes
    x.size = size(x.left) + size(x.right) + 1
    y.size = size(y.left) + size(y.right) + 1
 
    # Return new root
    return y

def insert(node: Optional[Node], key: Any, inversion_count: List) -> Node:
    """Insert a new key to the tree rooted with `node`.
    
    Meanwhile, update `inversion_count`.
    
    Note
    ----
    `inversion_count` is typed as a `List` since we need it to be mutable so that its value can be changed after each recursion call (while `int` is immutable).
    """     
    # 1. Perform the normal BST rotation
    if node is None:
        return Node(key)
 
    if key < node.key:
        node.left = insert(node.left, key, inversion_count)
 
        # To count inversions, for each inserted node, we need to find number of
        # elems greater than `key` that have been inserted before `key`.
        # Whenever inserting key < node, we go down left a level, so inversion_count 
        # increases by 1(node) + node.right.
        # Note: Here we only consider first-time insertion of a list into an 
        # empty tree. Subsequent delete/insert does not alter inversion_count.
        inversion_count[0] += size(node.right) + 1
    else:
        node.right = insert(node.right, key, inversion_count)
 
    # 2. Update height and size of this ancestor node
    node.height = max(height(node.left),   
                      height(node.right)) + 1
    node.size = size(node.left) + size(node.right) + 1
 
    # 3. Get the balance factor of this ancestor
    #     node to check whether this node became
    #    unbalanced
    balance = balance_factor(node)
 
    # If this node becomes unbalanced, 
    # then there are 4 cases
 
    # Left Left Case
    if (balance > 1 and key < node.left.key):
        return right_rotate(node)
 
    # Right Right Case
    if (balance < -1 and key > node.right.key):
        return left_rotate(node)
 
    # Left Right Case
    if balance > 1 and key > node.left.key:
        node.left = left_rotate(node.left)
        return right_rotate(node)
 
    # Right Left Case
    if balance < -1 and key < node.right.key:
        node.right = right_rotate(node.right)
        return left_rotate(node)
 
    # return the (unchanged) node pointer
    return node

def get_inversion_count(_list: List) -> int:
    """Count inversions in a list."""
    root = None # Create empty AVL Tree
 
    inversion_count = [0] # Initialize inversion_count
 
    # Starting from first element, insert all
    # elements one by one in an AVL tree.
    for item in _list: 
        # Note that address of inversion_count is passed
        # as insert operation updates inversion_count by
        # adding count of elements greater than
        # _list[i] on left of _list[i]
        root = insert(node=root, key=item, inversion_count=inversion_count)
 
    return inversion_count[0]

 
# Driver Code
if __name__ == '__main__':
    
    _list = [
        (23, "23"),
        (4, "4"),
        (30, "30"),
        (11, "11"),
        (7, "7"),
        (34, "34"),
        (20, "20"),
        (24, "24"),
        (22, "22"),
        (1, "1"),
    ]
    
    # Count inversions
    print("Number of inversions count are :", get_inversion_count(_list))
    
    # Display tree structure
    root: Node = None
    inversion_count = [0]
    for item in _list:
        root = insert(node=root, key=item[0], inversion_count=inversion_count)
    # Note: the following displayed tree is different from that from avl_tree.py.
    # Both are valid AVL trees, but the structures are different due to code 
    # implementation discrepencies.
    display_keys(root)