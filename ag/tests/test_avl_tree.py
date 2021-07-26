"""Unit tests for the AVL tree module."""

import random
import pytest

from forest import metrics
from forest import tree_exceptions
from forest.binary_trees import avl_tree
from forest.binary_trees import traversal

def test_simple_case(basic_tree):
    """Test the basic operations of an AVL tree."""
    tree = avl_tree.AVLTree()
    assert tree.empty

    # 23, 4, 30, 11, 7, 34, 20, 24, 22, 15, 1
    for key, data in basic_tree:
        tree.insert(key=key, data=data)

    assert tree.empty is False

    with pytest.raises(tree_exceptions.DuplicateKeyError):
        tree.insert(key=23, data="23")

    print(tree.inversion_count)
    assert tree.get_height(node=tree.root) == 3
    assert tree.get_leftmost(tree.root).key == 1
    assert tree.get_leftmost(tree.root).data == "1"
    assert tree.get_rightmost(tree.root).key == 34
    assert tree.get_rightmost(tree.root).data == "34"
    assert tree.search(24).key == 24
    assert tree.search(24).data == "24"
    node = tree.search(7)
    assert tree.get_successor(node).key == 11
    assert tree.get_predecessor(node).key == 4
    node = tree.search(15)
    assert tree.get_successor(node).key == 20
    node = tree.search(22)
    assert tree.get_predecessor(node).key == 20

    tree.delete(15)

    assert tree.search(15) is None


def test_deletion(basic_tree):
    """Test the deletion of an AVL tree."""
    tree = avl_tree.AVLTree()

    # 23, 4, 30, 11, 7, 34, 20, 24, 22, 15, 1
    for key, data in basic_tree:
        tree.insert(key=key, data=data)

    # No child
    tree.delete(15)
    assert [item for item in traversal.inorder_traverse(tree)] == [
        (1, "1"),
        (4, "4"),
        (7, "7"),
        (11, "11"),
        (20, "20"),
        (22, "22"),
        (23, "23"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ]

    # One right child
    tree.delete(7)
    assert [item for item in traversal.inorder_traverse(tree)] == [
        (1, "1"),
        (4, "4"),
        (11, "11"),
        (20, "20"),
        (22, "22"),
        (23, "23"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ]

    # One left child
    tree.insert(key=9, data="9")
    tree.delete(11)
    assert [item for item in traversal.inorder_traverse(tree)] == [
        (1, "1"),
        (4, "4"),
        (9, "9"),
        (20, "20"),
        (22, "22"),
        (23, "23"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ]

    # Two children
    tree.delete(23)
    assert [item for item in traversal.inorder_traverse(tree)] == [
        (1, "1"),
        (4, "4"),
        (9, "9"),
        (20, "20"),
        (22, "22"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ]


def test_deletion_no_child(basic_tree):
    """Test the deletion of an AVL tree."""
    tree = avl_tree.AVLTree()

    test_tree = [(23, "23"), (4, "4"), (30, "30"), (11, "11")]

    for key, data in test_tree:
        tree.insert(key=key, data=data)

    tree.delete(4)
    assert [item for item in traversal.inorder_traverse(tree)] == [
        (11, "11"),
        (23, "23"),
        (30, "30"),
    ]


def test_deletion_one_child(basic_tree):
    """Test the deletion of a red black tree."""
    tree = avl_tree.AVLTree()

    # 23, 4, 30, 11, 7, 34, 9
    test_tree = [
        (23, "23"),
        (4, "4"),
        (30, "30"),
        (11, "11"),
        (7, "7"),
        (34, "34"),
        (9, "9"),
    ]

    for key, data in test_tree:
        tree.insert(key=key, data=data)

    tree.delete(11)
    assert [item for item in traversal.inorder_traverse(tree)] == [
        (4, "4"),
        (7, "7"),
        (9, "9"),
        (23, "23"),
        (30, "30"),
        (34, "34"),
    ]


def test_deletion_two_children(basic_tree):
    """Test the deletion of a red black tree."""
    tree = avl_tree.AVLTree()

    test_tree = [
        (23, "23"),
        (4, "4"),
        (30, "30"),
        (11, "11"),
        (7, "7"),
        (34, "34"),
        (9, "9"),
        (27, "27"),
    ]

    for key, data in test_tree:
        tree.insert(key=key, data=data)

    tree.delete(23)
    assert [item for item in traversal.inorder_traverse(tree)] == [
        (4, "4"),
        (7, "7"),
        (9, "9"),
        (11, "11"),
        (27, "27"),
        (30, "30"),
        (34, "34"),
    ]


def test_traversal(basic_tree):
    """Test tree traversal."""
    tree = avl_tree.AVLTree()

    for key, data in basic_tree:
        tree.insert(key=key, data=data)

    assert [item for item in traversal.inorder_traverse(tree)] == [
        (1, "1"),
        (4, "4"),
        (7, "7"),
        (11, "11"),
        (15, "15"),
        (20, "20"),
        (22, "22"),
        (23, "23"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ]

    assert [item for item in traversal.preorder_traverse(tree)] == [(23, '23'), (11, '11'), (4, '4'), (1, '1'), (7, '7'), (20, '20'), (15, '15'), (22, '22'), (30, '30'), (24, '24'), (34, '34')]

    assert [item for item in traversal.postorder_traverse(tree)] == [(1, '1'), (7, '7'), (4, '4'), (15, '15'), (22, '22'), (20, '20'), (11, '11'), (24, '24'), (34, '34'), (30, '30'), (23, '23')]
    
    assert [item for item in traversal.levelorder_traverse(tree)] == [(23, '23'), (11, '11'), (30, '30'), (4, '4'), (20, '20'), (24, '24'), (34, '34'), (1, '1'), (7, '7'), (15, '15'), (22, '22')]
def test_binary_search_tree_traversal_random():
    """Test BST traversal with random samples."""
    for _ in range(0, 10):
        # random sampling of 1000 unique elems without replacement from [1,2000)
        insert_data = random.sample(range(1, 2000), 1000)        
        tree = avl_tree.AVLTree()
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

def test_random_insert_delete_both():
    """Test random insert and delete."""
    for _ in range(0, 10):
        insert_data = random.sample(range(1, 2000), 1000)
        delete_data = random.sample(insert_data, 500)

        tree = avl_tree.AVLTree()
        for key in insert_data:
            tree.insert(key=key, data=str(key))

        for key in delete_data:
            tree.delete(key=key)

        # we only care about the key of the traverse
        result = [item for item, _ in traversal.inorder_traverse(tree)]
        result_reverse = [item for item, _ in traversal.reverse_inorder_traverse(tree)]
        
        remaining_data = [item for item in insert_data if item not in delete_data]
        remaining_data.sort()  # sorts a list in ascending order
        assert result == remaining_data
        remaining_data.sort(reverse=True)
        assert result_reverse == remaining_data


def test_metrics(basic_tree):
    """Test AVL tree with metrics enabled."""
    registry = metrics.MetricRegistry()
    tree = avl_tree.AVLTree(registry=registry)
    
    for key, data in basic_tree:
        tree.insert(key=key, data=data)
    
    # Assert the following will return non-None results
    assert registry.get_metric(name="avlt.rotate").count
    assert registry.get_metric(name="avlt.height").report()
 