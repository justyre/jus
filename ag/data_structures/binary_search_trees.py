# Create a data structure which can store ~100M records &
# perform insertion, search, update and list operations efficiently 
# using balanced binary search tree (aka balanced BST)

"""Binary search tree implementation."""

class User:
    """User."""
    
    # constructor method
    def __init__(self, username, name, email) -> None:
        self.username = username
        self.name = name
        self.email = email
        # print('User created!')
    
    def __repr__(self) -> str:
        """Override the default representation func (returning an official str repr)."""
        return "User(username='{}', name='{}', email='{}')".format(self.username, self.name, self.email)
    
    def __str__(self) -> str:
        """Override the default string function, returning a human-readable format."""
        return self.__repr__()
    
    def introduce_yourself(self, guest_name):
        """Print a self-introducing sentence."""
        print("Hi {}, I'm {}! Contact me at {} .".format(guest_name, self.name, self.email))


class UserDatabase:
    """Linear data structure (ie brute force)."""
    
    # self.users is an asc sorted list initialized as an empty one
    def __init__(self) -> None:
        self.users = []
        
    def insert(self, user):
        """Loop through the list and add the new user at a position that keeps the list sorted. O(N)."""
        i = 0
        while i < len(self.users):
            # eg. if [0]'s username > `user.username`, break out of loop, 
            # and put [user] ahead of [0] as the new [0]
            if self.users[i].username > user.username:
                break
            i += 1
        # use Python's list insert() method (the inserted elem is at new pos i).
        # if inserting `user` > all existing elems, i = len(self.users), ie last
        # note: `i` must be initialized outside loop, or we'll have 
        # UnboundLocalError. That's why we can only use while-loop, not for-loop
        self.users.insert(i, user)
    
    def find(self, username):
        """Loop through the list and find the obj w/username matching `username`. O(N)."""
        for user in self.users:
            if user.username == username:
                return user
    
    def update(self, user):
        """Loop through the list and find the obj matching username and update the details. O(N)."""
        target = self.find(user.username)
        target.name, target.email = user.name, user.email
    
    def list_all(self):
        """Return the list of user objs. O(1)."""
        return self.users

class TreeNode:
    """A node within a binary tree, w/many methods encapsulated."""
    
    def __init__(self, key) -> None:
        self.key = key
        self.left = None
        self.right = None
        
    def height(self):
        """Compute the height (aka depth) of a binary tree."""
        # the height/depth is defined as the total levels of the longest path from 
        # the root node to a leaf
        if self is None:
            return 0
        # note: in the next line, cannot use self.left.height() instead, coz 
        # when self.left None, self.left.height() will throw AttributeError
        # `NoneType has no attribute `height```
        return 1 + max(TreeNode.height(self.left), TreeNode.height(self.right))

    def size(self):
        """Compute total # (non-None) nodes in a binary tree (including the root)."""
        if self is None:
            return 0
        return 1 + TreeNode.size(self.left) + TreeNode.size(self.right)

    def traverse_in_order(self):
        """Inorder traversal of a binary tree, returns a list (LDR)."""
        if self is None:
            return []
        return TreeNode.traverse_in_order(self.left) + [self.key] + TreeNode.traverse_in_order(self.right)
    
    def traverse_pre_order(self):
        """Preorder traversal (DLR)."""
        # traverse the current node, then the left subtree recursively preorder 
        # (ie from root to leaf), then the right subtree recursively preorder.
        if self is None:
            return []
        return [self.key] + TreeNode.traverse_pre_order(self.left) + TreeNode.traverse_pre_order(self.right)

    def traverse_post_order(self):
        """Postorder traversal (LRD)."""
        if self is None:
            return []
        return TreeNode.traverse_post_order(self.left) + TreeNode.traverse_post_order(self.right) + [self.key]
    
    def display_keys(self, space='\t', level=0):
        """Display all the keys in a TreeNode obj for easier visualization."""
        # debugcode next line
        # print(node.key if node else None, level)
        # if the node is empty, print the empty set symbol
        if self is None:
            print(space * level + '∅')
            return
        
        # if the node is a leaf, print node.key
        if self.left is None and self.right is None:
            print(space * level + str(self.key))
            return
        
        # if the node has children, show right subtree up, left subtree down
        TreeNode.display_keys(self.right, space, level + 1)
        print(space * level + str(self.key))
        TreeNode.display_keys(self.left, space, level + 1)

    def to_tuple(self):
        """Convert a binary tree into a tuple. Inverse of `parse_tuple()`."""
        # if the node is empty
        if self is None:
            return None
        # if the node is a leaf
        if self.left is None and self.right is None:
            return self.key
        # don't need an `else` here, coz two prev ifs have all returned
        left_subtree = TreeNode.to_tuple(self.left)
        right_subtree = TreeNode.to_tuple(self.right)
        return (left_subtree, self.key, right_subtree)

    def __repr__(self) -> str:
        """Overload the default representation func (returning an official str repr)."""
        return "BinaryTree <{}>".format(self.to_tuple())
    
    def __str__(self) -> str:
        """Return a human-readable format."""
        return self.__repr__()

    @staticmethod
    def parse_tuple(data):
        """Parse a tuple (left_subtree, key, right_subtree) into a binary tree."""
        # Note: Here we use the @staticmethod decorator, which means: this method 
        # cannot have self or cls as parameter; it cannot access the class 
        # attributes or methods, or the instance attributes or methods.
        # You can call a static method directly like TreeNode.parse_tuple(data), 
        # w/out making an instance first. (For non-static methods, this will err)
        if data is None:
            node = None
        elif isinstance(data, tuple) and len(data) == 3:
            node = TreeNode(data[1])
            node.left = TreeNode.parse_tuple(data[0])
            node.right = TreeNode.parse_tuple(data[2])
        # we don't think input tuple is malformed, so 
        # len(data) == 0(None), 1(this), 3. No other possibilities.
        # note: a one-elem "tuple" is not an instance of tuple, it's just an int
        else:
            node = TreeNode(data)
        return node

def remove_none(nums):
    """Get a list without Nones. Input `nums` can be list or tuple."""
    return [x for x in nums if x is not None]

def is_bst(node):
    """Check if a node is a binary search tree."""
    # A binary tree satisfies:
    # the left subtree of any node only contains nodes w/keys < this node's key, & 
    # the right subtree .. > ..
    # From this, we can see that if a parent node is a BST, then both its left & 
    # right subtrees must be BSTs too.
    # returns a tuple of (True/False, min of keys in node, max of keys in node)
    if node is None:
        return True, None, None
    
    is_bst_l, min_l, max_l = is_bst(node.left)
    is_bst_r, min_r, max_r = is_bst(node.right)
    is_bst_node = (is_bst_l and is_bst_r and (max_l is None or max_l < node.key) and (min_r is None or min_r > node.key))
    
    min_key = min(remove_none([min_l, node.key, min_r]))
    max_key = max(remove_none([max_l, node.key, max_r]))
    # debugcode
    # print(node.key, is_bst_node, min_key, max_key)
    
    return is_bst_node, min_key, max_key


class BSTNode:
    """A node of a binary search tree."""
    
    def __init__(self, key, value=None) -> None:
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

def insert(node, key, value):
    """Insert a new node(key, value) into a BST."""
    # Time complexity: O(log N) + O(N) = O(N) (coz worst case height of tree = N)
    if node is None:
        node = BSTNode(key, value)
    elif key < node.key:
        # replace the orig node.left w/the new node.left(w/inserted node)
        node.left = insert(node.left, key, value)
        node.left.parent = node
    elif key > node.key:
        node.right = insert(node.right, key, value)
        node.right.parent = node
        
    return node
 
def find(node, key):
    """Find a node with a given key within a BST."""
    # For a balanced BST, this func only takes O(log N); otherwise it's O(N)
    if node is None:
        return None
    if key == node.key:
        return node
    if key < node.key:
        return find(node.left, key)
    if key > node.key:
        return find(node.right, key)

def update(node, key, value):
    """Update a node with a given key with `value` within a BST."""
    # For a balanced BST, this func only takes O(log N); otherwise it's O(N)
    target = find(node, key)
    if target is not None:
        target.value = value

def list_all(node):
    """Retrieve all the key-value pairs in a BST in asc sorted order of keys."""
    # To achieve asc sortedness, we can perform an inorder traversal of the BST, 
    # and then we know from the definition of BST (cf is_bst()) that it's asc. O(N)
    if node is None:
        return []
    return list_all(node.left) + [(node.key, node.value)] + list_all(node.right)    

def is_balanced(node):
    """Check if a BST is balanced; returns (True/False, height of tree)."""
    # First we ensure the left subtree is balanced; then ensure the right subtree 
    # is balanced too; and ensure the diff betw heights of left & right subtree <=1
    if node is None:
        return True, 0
    balanced_l, height_l = is_balanced(node.left)
    balanced_r, height_r = is_balanced(node.right)
    balanced = balanced_l and balanced_r and abs(height_l - height_r) <= 1
    height = 1 + max(height_l, height_r)
    return balanced, height

def create_balanced_bst(data, lo=0, hi=None, parent=None):
    """Create a balanced BST from an asc sorted list/array of key-value pairs."""
    # To do this, first we find the midpoint of the list, and make it the root;
    # then we balance the left sublist; then the right sublist.
    
    # Set the default of `hi` to the last index of elems in `data`.
    # Letting `hi` to be a parameter gives user customization power
    if hi is None:
        hi = len(data) - 1
    # for inverted indices, return None
    if lo > hi:
        return None
    
    mid = (lo + hi) // 2
    key, value = data[mid]
    
    root = BSTNode(key, value)
    root.parent = parent
    # the next line shows why we need `parent` as a parameter --
    # we need to tell a balanced subtree where to point itself
    root.left = create_balanced_bst(data, lo, mid - 1, root)
    root.right = create_balanced_bst(data, mid + 1, hi, root)
    return root
 
def balance_bst(node):
    """Balance an unbalanced BST."""
    # By first performing an inorder traversal of it, 
    # so we have an asc sorted list now, where we then create_balance_bst() from
    return create_balanced_bst(list_all(node))


###############################

class TreeMap:
    """A generic class for BST that has been stated in a python-friendly manner."""
    
    def __init__(self) -> None:
        # self.root is the BSTNode we are working on
        self.root = None
    
    def __setitem__(self, key, value):
        """With this, we can set a node by `treemap['key']`.
        
        If it doesn't exist, we insert it; if it already exists, we update it.
        """
        node = find(self.root, key)
        # below is the same as `if node is None`, coz `not None == True`
        if not node:
            self.root = insert(self.root, key, value)
            self.root = balance_bst(self.root)
        else:
            update(self.root, key, value)
    
    def __getitem__(self, key):
        """With this, we can get a node by `treemap['key']`."""
        node = find(self.root, key)
        return node.value if node else None
    
    def __iter__(self):
        """With this, we can iterate by `for key, value in treemap:` (in asc order)."""
        return (x for x in list_all(self.root))
    
    def __len__(self):
        """With this, we can get the length of a node by `len(treemap)`."""
        return TreeNode.size(self.root)
    
    def display(self):
        """Display the tree nicely."""
        return TreeNode.display_keys(self.root)
    

#########################
# Driver code

# User and UserDatabase

aakash = User('aakash', 'Aakash Rai', 'aakash@example.com')
biraj = User('biraj', 'Biraj Das', 'biraj@example.com')
hemanth = User('hemanth', 'Hemanth Jain', 'hemanth@example.com')
jadhesh = User('jadhesh', 'Jadhesh Verma', 'jadhesh@example.com')
siddhant = User('siddhant', 'Siddhant Sinha', 'siddhant@example.com')
sonaksh = User('sonaksh', 'Sonaksh Kumar', 'sonaksh@example.com')
vishal = User('vishal', 'Vishal Goel', 'vishal@example.com')

users = [aakash, biraj, hemanth, jadhesh, siddhant, sonaksh, vishal]

db = UserDatabase()
db.insert(hemanth)
db.insert(aakash)
db.insert(vishal)
print(db.users)
db.update(User(username='aakash', name='Aakash U', email='aakashu@example.com'))
user = db.find('aakash')
print(user)
db.insert(siddhant)
print(db.list_all())


# TreeNode

tree2 = TreeNode.parse_tuple(((1, 2, None), 3, ((None, 4, 5), 6, (7, 8, 9))))
print(tree2)
print(type(tree2), tree2.height(), tree2.size())
print(tree2.traverse_in_order())
print(tree2.traverse_pre_order())
print(tree2.traverse_post_order())
# should show tree2 in tree form that is rotated 90 degrees counterclockwise 
TreeNode.display_keys(tree2)
# should show tree2 in tuple form
print(TreeNode.to_tuple(tree2))

print(is_bst(tree2))
    
tree2 = insert(None, aakash.username, aakash)
insert(tree2, biraj.username, biraj)
insert(tree2, hemanth.username, hemanth)
insert(tree2, jadhesh.username, jadhesh)
insert(tree2, siddhant.username, siddhant)
insert(tree2, sonaksh.username, sonaksh)
insert(tree2, vishal.username, vishal)
TreeNode.display_keys(tree2)
print(TreeNode.height(tree2))

node = find(tree2, 'hemanth')
print(node.key, node.value)

update(tree2, 'biraj', User('biraj', 'Biraj J', 'birajj@example.com'))
node = find(tree2, 'biraj')
print(node.value)

print(list_all(tree2))
print(is_balanced(tree2))

data = [(user.username, user) for user in users]
tree = create_balanced_bst(data)
TreeNode.display_keys(tree)

tree1 = None
for user in users:
    tree1 = insert(tree1, user.username, user)
TreeNode.display_keys(tree1)
tree2 = balance_bst(tree1)
TreeNode.display_keys(tree2)


# BSTNode

tree = BSTNode(jadhesh.username, jadhesh)
print(tree.key, tree.value)


# TreeMap

treemap = TreeMap()
treemap.display()

for user in users:
    # below uses TreeMap.__setitem__()
    treemap[user.username] = user
treemap.display()

# below uses TreeMap.__getitem__()
print(treemap['jadhesh'])
# below uses TreeMap.__len__()
print(len(treemap))

# below uses TreeMap.__iter__()
for key, value in treemap:
    print(key, value)
# below uses TreeMap.__iter__(), too
print(list(treemap))
