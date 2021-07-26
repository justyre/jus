"""Unit tests for the traversal module."""

import random

from forest.binary_trees import binary_search_tree
from forest.binary_trees import traversal


def test_binary_search_tree_traversal(test_tree_inorder_postorder: list, test_tree_reverse_inorder: list, basic_tree: list) -> None:
    """Test binary search tree traversal."""
    # Case 1: The inorder and postorder cases
    
    tree = binary_search_tree.BinarySearchTree()

    for key, data in test_tree_inorder_postorder:
        tree.insert(key=key, data=data)
        
    assert [item for item in traversal.inorder_traverse(tree)] == [
        (1, '34'), (2, '7'), (3, '30'), (4, '11'), (5, ''), (6, '4')
    ]

    assert [item for item in traversal.inorder_traverse(tree, False)] == [
        (1, '34'), (2, '7'), (3, '30'), (4, '11'), (5, ''), (6, '4')
    ]
    
    assert [item for item in traversal.postorder_traverse(tree)] == [
        (1, '34'), (2, '7'), (4, '11'), (3, '30'), (6, '4'), (5, '')
    ]
   
    assert [item for item in traversal.postorder_traverse(tree, False)] == [
        (1, '34'), (2, '7'), (4, '11'), (3, '30'), (6, '4'), (5, '')
    ]
    
    # Case 2: The reverse inorder cases
    
    tree = binary_search_tree.BinarySearchTree()

    for key, data in test_tree_reverse_inorder:
        tree.insert(key=key, data=data)
        
    assert [item for item in traversal.reverse_inorder_traverse(tree)] == [
        (6, '34'), (5, '7'), (4, '30'), (3, '11'), (2, ''), (1, '4')
    ]

    assert [item for item in traversal.reverse_inorder_traverse(tree, False)] == [
        (6, '34'), (5, '7'), (4, '30'), (3, '11'), (2, ''), (1, '4')
    ]
    
    # Case 3: The preorder and levelorder cases (using basic_tree)
    
    tree = binary_search_tree.BinarySearchTree()

    for key, data in basic_tree:
        tree.insert(key=key, data=data)
    
    assert [item for item in traversal.preorder_traverse(tree)] == [
        (23, '23'), (4, '4'), (1, '1'), (11, '11'), (7, '7'), 
        (20, '20'), (15, '15'), (22, '22'), (30, '30'), (24, '24'), (34, '34'),
    ]

    assert [item for item in traversal.preorder_traverse(tree, False)] == [
        (23, '23'), (4, '4'), (1, '1'), (11, '11'), (7, '7'), 
        (20, '20'), (15, '15'), (22, '22'), (30, '30'), (24, '24'), (34, '34'),
    ]

    assert [item for item in traversal.levelorder_traverse(tree)] == [
        (23, '23'), (4, '4'), (30, '30'), (1, '1'), (11, '11'), 
        (24, '24'), (34, '34'), (7, '7'), (20, '20'), (15, '15'), (22, '22'),
    ]


def test_binary_search_tree_traversal_random():
    """Test BST traversal with random samples."""
    for _ in range(0, 10):
        # random sampling of 1000 unique elems without replacement from [1,2000)
        insert_data = random.sample(range(1, 2000), 1000)
        
        tree = binary_search_tree.BinarySearchTree()
        for key in insert_data:
            tree.insert(key=key, data="")  # data does not matter
        
        preorder_recursive = [item for item in traversal.preorder_traverse(tree, True)]
        preorder_nonrecursive = [item for item in traversal.preorder_traverse(tree, False)]
        assert preorder_recursive == preorder_nonrecursive
        
        inorder_recursive = [item for item in traversal.inorder_traverse(tree, True)]
        inorder_nonrecursive = [
            item for item in traversal.inorder_traverse(tree, False)
        ]
        assert inorder_recursive == inorder_nonrecursive

        rinorder_recursive = [
            item for item in traversal.reverse_inorder_traverse(tree, True)
        ]
        rinorder_nonrecursive = [
            item for item in traversal.reverse_inorder_traverse(tree, False)
        ]
        assert rinorder_recursive == rinorder_nonrecursive

        postorder_recursive = [
            item for item in traversal.postorder_traverse(tree, True)
        ]
        postorder_nonrecursive = [
            item for item in traversal.postorder_traverse(tree, False)
        ]
        assert postorder_recursive == postorder_nonrecursive        
          