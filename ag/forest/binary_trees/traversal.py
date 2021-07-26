# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Binary tree traversal.

Routines
--------
inorder_traverse(tree: `SupportedTreeType`, recursive: `bool`)
    Perform in-order traversal.
preorder_traverse(tree: `SupportedTreeType`, recursive: `bool`)
    Perform pre-order traversal.
postorder_traverse(tree: SupportedTreeType, recursive: `bool`)
    Perform post-order traversal.
"""
# Time complexity for these traversals are all O(N).
# Space complexity for both recursive and non-recursive traversals: 
# Average O(log N), worst case O(N), except for the level-order traversal, 
# whose best case space complexity is O(1) (when each level has only one node) and 
# the worst case O(N).

from typing import Any, Iterator, Union

from forest.binary_trees import avl_tree
from forest.binary_trees import binary_search_tree
from forest.binary_trees import binary_tree

# Alias for the supported node types.  For type checking.
SupportedNodeType = Union[None, binary_search_tree.Node, avl_tree.Node]
"""Alias for the supported tree node types. For type checking."""

SupportedTreeType = Union[binary_search_tree.BinarySearchTree, avl_tree.AVLTree]
"""Alias for the supported tree types. For type checking."""


def inorder_traverse(
    tree: SupportedTreeType, recursive: bool = True
) -> binary_tree.Pairs:
    """Perform in-order traversal, a kind of depth-first traversal.
    
    In-order traversal traverses a tree by the order: 
    left subtree, current node, right subtree (ie LDR)
    
    Parameters
    ----------
    tree: `SupportedTreeType`
        An instance of the supported binary tree types.
    recursive: `bool`
        Perform traversal recursively or not.
    
    Yields (as an Iterator)
    ------
    `Pairs`
        The next (key, data) pair in the in-order traversal.
        
    Examples
    --------
    >>> from forest.binary_trees import binary_search_tree
    >>> from forest.binary_trees import traversal
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
    >>> [item for item in traversal.inorder_traverse(tree)]
    [(1, '1'), (4, '4'), (7, '7'), (11, '11'), (15, '15'), (20, '20'),
     (22, '22'), (23, '23'), (24, '24'), (30, '30'), (34, '34')]   
    """
    if recursive:
        return _inorder_traverse(node=tree.root)
    return _inorder_traverse_non_recursive(root=tree.root)


def reverse_inorder_traverse(
    tree: SupportedTreeType, recursive: bool = True
) -> binary_tree.Pairs:
    """Perform reversed in-order traversal.
    
    Reversed in-order traversal traverses a tree by the order:
    right subtree, current node, left subtree (RDL)
    
    Parameters
    ----------
    tree : `SupportedTreeType`
        An instance of the supported binary tree types.
    recursive: `bool`
        Perform traversal recursively or not.
        
    Yields
    ------
    `Pairs`
        The next (key, data) pair in the reversed in-order traversal.
        
    Examples
    --------
    >>> from forest.binary_trees import binary_search_tree
    >>> from forest.binary_trees import traversal
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
    >>> [item for item in traversal.reverse_inorder_traverse(tree)]
    [(34, '34'), (30, '30'), (24, '24'), (23, '23'), (22, '22'), (20, '20'),
     (15, '15'), (11, '11'), (7, '7'), (4, '4'), (1, '1')]
    """
    if recursive:
        return _reverse_inorder_traverse(node=tree.root)
    return _reverse_inorder_traverse_non_recursive(root=tree.root)    


def preorder_traverse(
    tree: SupportedTreeType, recursive: bool = True
) -> binary_tree.Pairs:
    """Perform Pre-Order traversal.
    
    Pre-order traversal traverses a tree by the order:
    current node, left subtree, right subtree (DLR)
    
    Parameters
    ----------
    tree : `SupportedTreeType`
        An instance of the supported binary tree types.
    recursive: `bool`
        Perform traversal recursively or not.
        
    Yields
    ------
    `Pairs`
        The next (key, data) pair in the pre-order traversal.
        
    Examples
    --------
    >>> from forest.binary_trees import binary_search_tree
    >>> from forest.binary_trees import traversal
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
    >>> [item for item in traversal.preorder_traverse(tree)]
    [(23, '23'), (4, '4'), (1, '1'), (11, '11'), (7, '7'), (20, '20'),
     (15, '15'), (22, '22'), (30, '30'), (24, '24'), (34, '34')]
    """
    if recursive:
        return _preorder_traverse(node=tree.root)
    return _preorder_traverse_non_recursive(root=tree.root)    


def postorder_traverse(
    tree: SupportedTreeType, recursive: bool = True
) -> binary_tree.Pairs:
    """Perform Post-Order traversal.
    
    Post-order traversal traverses a tree by the order:
    left subtree, right subtree, current node (LRD)
    
    Parameters
    ----------
    tree : `SupportedTreeType`
        An instance of the supported binary tree types.
    recursive: `bool`
        Perform traversal recursively or not.
        
    Yields
    ------
    `Pairs`
        The next (key, data) pair in the post-order traversal.
        
    Examples
    --------
    >>> from forest.binary_trees import binary_search_tree
    >>> from forest.binary_trees import traversal
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
    >>> [item for item in traversal.postorder_traverse(tree)]
    [(1, '1'), (7, '7'), (15, '15'), (22, '22'), (20, '20'), (11, '11'),
     (4, '4'), (24, '24'), (34, '34'), (30, '30'), (23, '23')]
    """
    if recursive:
        return _postorder_traverse(node=tree.root)
    return _postorder_traverse_non_recursive(root=tree.root)


def levelorder_traverse(tree: SupportedTreeType) -> binary_tree.Pairs:
    """Perform Level-Order traversal.
    
    Level-order traversal traverses a tree in the following order:
    level by level, from left to right, starting from the root node.
    
    Parameters
    ----------
    tree : `SupportedTreeType`
        An instance of the supported binary tree types.
        
    Yields
    ------
    `Pairs`
        The next (key, data) pair in the level-order traversal.
        
    Examples
    --------
    >>> from forest.binary_trees import binary_search_tree
    >>> from forest.binary_trees import traversal
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
    >>> [item for item in traversal.levelorder_traverse(tree)]
    [(23, '23'), (4, '4'), (30, '30'), (1, '1'), (11, '11'), (24, '24'),
     (34, '34'), (7, '7'), (20, '20'), (15, '15'), (22, '22')]
    """
    queue = [tree.root]
    while len(queue) > 0:
        temp = queue.pop(0)
        # `temp` is the first elem of `queue` (since pop(0));
        # `queue` is now without its original first elem (ie popped is deleted)
        yield (temp.key, temp.data)
        # Because stack `queue` is FIFO, insert left child before right child.
        if temp.left:
            queue.append(temp.left)
        if temp.right:
            queue.append(temp.right)
                

def _inorder_traverse(node: SupportedNodeType) -> binary_tree.Pairs:
    if node:
        yield from _inorder_traverse(node.left)
        yield (node.key, node.data)
        yield from _inorder_traverse(node.right)


def _inorder_traverse_non_recursive(root: SupportedNodeType) -> binary_tree.Pairs:
    # An internal generator function (coz returning Pairs is an iterator). 
    # The algorithm is: (Remember that we want the final order to be LDR)
    # 1. Create a stack. If the current node has a right child, we push (ie append) 
    #    its right child to the stack and then push the node itself to the stack.
    # 2. Then we move to current.left, and repeat Step 1.
    # 3. When a node is popped from the stack, we produce the node if (the node has 
    #    no right child) or (the node == the top root node).
    if root is None:
        raise StopIteration
    
    stack = []
    if root.right:
        stack.append(root.right)    
    stack.append(root)
    current = root.left
    
    while True:
        if current:
            if current.right:
                stack.append(current.right)
                stack.append(current)
                current = current.left
                continue  # this skips all the rest statements in the while-True loop
            # If c.r is None, first we squeeze c into stack, then we move to c.l
            stack.append(current)
            current = current.left
        
        else:
            # If c is None, we are at the (locally) leftmost node
            if stack:
                # For a list, `if stack` means if it is non-empty (ie len(stack)>0).
                # pop() returns the last value of a list. So if c is None, it means we 
                # had gone left one step too deep, so we retreat by one step by popping
                current = stack.pop()  
                if current.right is None:
                    # We know that stack.pop() is c.parent, since c is its left child. 
                    # So if c.parent.right is None, and c is None (remember that we are
                    # in the upmost `else`), we only need to yield c.parent, which is 
                    # the now `current`. Then we set c to None again, so we go back to 
                    # the start of this upmost `else` clause
                    yield (current.key, current.data)
                    current = None
                    continue
                else:
                    if stack:
                        if current.right == stack[-1]:
                            # If c.r is the last in stack, the stack used to be [.., 
                            # c.r, c]. Since c < c.r, we yield c first, and use c.r as 
                            # the new c (and pop it out of stack)
                            yield (current.key, current.data)
                            current = stack.pop()
                            continue
                        else:
                            # If current.right != stack[-1], ie there are more nodes on 
                            # the right, so we keep the current and go back to add them.
                            continue
            else:
                break  # coz stack is empty. `break` terminates the innermost loop


def _reverse_inorder_traverse(node: SupportedNodeType) -> binary_tree.Pairs:
    if node:
        yield from _reverse_inorder_traverse(node.right)
        yield (node.key, node.data)
        yield from _reverse_inorder_traverse(node.left)


def _reverse_inorder_traverse_non_recursive(
    root: SupportedNodeType
) -> binary_tree.Pairs:
    # RDL
    if root is None:
        raise StopIteration

    stack = []
    if root.left:
        stack.append(root.left)    
    stack.append(root)
    current = root.right

    while True:

        if current:
            if current.left:
                stack.append(current.left)
                stack.append(current)
                current = current.right
                continue
            stack.append(current)
            current = current.right

        else:
            # If current is None
            if stack:
                current = stack.pop()

                if current.left is None:
                    yield (current.key, current.data)
                    current = None
                    continue
                else:  # current.right is not None
                    if stack:
                        if current.left == stack[-1]:
                            yield (current.key, current.data)
                            current = stack.pop()
                            continue
                        else:  
                            # If c.r is not the last elem of stack:
                            # This case means there are more nodes on the right, so we
                            # keep the current and go back to add them.
                            continue

            else:  # stack is empty
                break


def _preorder_traverse(node: SupportedNodeType) -> binary_tree.Pairs:
    if node:
        yield (node.key, node.data)
        yield from _preorder_traverse(node.left)
        yield from _preorder_traverse(node.right)


def _preorder_traverse_non_recursive(root: SupportedNodeType) -> binary_tree.Pairs:
    # The algorithm is:
    # 1. When we visit a node, we push it to the stack, then push its right child to 
    # the stack, and then push its left child to the stack.
    # 2. When a node is popped (ie deleted) from the stack, we produce the node.
    if root is None:
        raise StopIteration

    stack = [root]

    while stack:
        temp = stack.pop()
        # `temp` is the last elem of `stack`;
        # `stack` is now without its original last elem (ie popped is deleted)
        yield (temp.key, temp.data)

        # Because stack is FILO, insert right child before left child.
        if temp.right:
            stack.append(temp.right)

        if temp.left:
            stack.append(temp.left)


def _postorder_traverse(node: SupportedNodeType) -> binary_tree.Pairs:
    if node:
        yield from _postorder_traverse(node.left)
        yield from _postorder_traverse(node.right)
        yield (node.key, node.data)
        

def _postorder_traverse_non_recursive(root: SupportedNodeType) -> binary_tree.Pairs:
    # LRD
    if root is None:
        raise StopIteration

    stack = []
    if root.right:
        stack.append(root.right)
    stack.append(root)
    current = root.left

    while True:

        if current:
            if current.right:
                stack.append(current.right)
                stack.append(current)
                current = current.left
                continue
            else:
                # If current.right is None
                if current.left:
                    stack.append(current)
                else:
                    # When c.r and c.l are both None, c is leaf, so it can be yielded
                    yield (current.key, current.data)
                current = current.left

        else:
            # If current is None
            if stack:
                current = stack.pop()

                if current.right is None:
                    # Since we're doing LRD, if there's no R, we can yield D
                    yield (current.key, current.data)
                    current = None
                else:
                    # If current.right is not None
                    if stack:
                        if current.right != stack[-1]:
                            # If stack[-1] is not c.r, c.r must have been popped and 
                            # yielded, so we can yield c now
                            yield (current.key, current.data)
                            current = None
                        else:
                            # Then c is the `D` of a local `LRD`. We need to swap 
                            # `current` and `stack[-1]`, since stack[-1] is c.r and we 
                            # only want nodes with heights <= c's in the stack. Thus, 
                            # with new current as the old c.r, we can track down the 
                            # right subtree of the old current node
                            temp = stack.pop()
                            stack.append(current)
                            current = temp

                    else:
                        # If stack is empty
                        yield (current.key, current.data)
                        break
            else:
                # If stack is empty
                break
   
    
                        

# # test client
                
# from forest.binary_trees import binary_search_tree
# tree = binary_search_tree.BinarySearchTree()
# # tree.insert(key=5, data="")
# # tree.insert(key=6, data="4")
# # tree.insert(key=3, data="30")
# # tree.insert(key=4, data="11")
# # tree.insert(key=2, data="7")
# # tree.insert(key=1, data="34")
# tree.insert(key=6, data='')
# tree.insert(key=4, data='')
# tree.insert(key=7, data='')
# tree.insert(key=1, data='')
# tree.insert(key=5, data='')
# tree.insert(key=10, data='')
# tree.insert(key=3, data='')
# tree.insert(key=8, data='')
# tree.insert(key=2, data='')
# tree.insert(key=9, data='')
# tree.root.display_keys()
# print([item for item in inorder_traverse(tree, recursive=True)])
# print([item for item in inorder_traverse(tree, recursive=False)])
# print([item for item in postorder_traverse(tree, recursive=True)])
# print([item for item in postorder_traverse(tree, recursive=False)])
# print()

# tree = binary_search_tree.BinarySearchTree()
# tree.insert(key=2, data="")
# tree.insert(key=1, data="4")
# tree.insert(key=4, data="30")
# tree.insert(key=3, data="11")
# tree.insert(key=5, data="7")
# tree.insert(key=6, data="34")
# tree.root.display_keys()
# print([item for item in reverse_inorder_traverse(tree, recursive=True)])
# print([item for item in reverse_inorder_traverse(tree, recursive=False)])
# print()

# treelist = [
#         (23, "23"),
#         (4, "4"),
#         (30, "30"),
#         (11, "11"),
#         (7, "7"),
#         (34, "34"),
#         (20, "20"),
#         (24, "24"),
#         (22, "22"),
#         (15, "15"),
#         (1, "1"),
#     ]

# tree = binary_search_tree.BinarySearchTree()

# for key, data in treelist:
#     tree.insert(key=key, data=data)
# tree.root.display_keys()
# print([item for item in levelorder_traverse(tree)])
