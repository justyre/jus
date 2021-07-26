"""Unit tests for the single threaded binary search tree module."""

import random

from forest.binary_trees import single_threaded_binary_trees


def test_right_threaded_tree(test_single_threaded_tree: list) -> None:
    """Test the basic opeartions of a binary search tree."""
    tree = single_threaded_binary_trees.RightThreadedBinaryTree()

    assert tree.empty

    for key, data in test_single_threaded_tree:
        tree.insert(key=key, data=data)

    assert tree.empty is False
    assert list(tree.inorder_traverse()) == [(1, ''), (2, ''), (3, ''), (4, ''), (5, ''), (6, ''), (7, ''), (8, '')]
    tree.delete(7)
    assert list(tree.preorder_traverse()) == [(4, ''), (1, ''), (3, ''), (2, ''), (8, ''), (5, ''), (6, '')]
    assert tree.search(3).right.key == 4    
    assert tree.get_leftmost(node=tree.root).key == 1
    assert tree.get_rightmost(node=tree.root).key == 8
    assert tree.get_height(node=tree.root) == 3
    assert tree.get_predecessor(node=tree.root).key == 3
    temp = tree.search(key=5)
    assert tree.get_successor(node=temp).key == 6

def test_left_threaded_tree(test_single_threaded_tree: list) -> None:
    """Test the basic opeartions of a binary search tree."""
    tree = single_threaded_binary_trees.LeftThreadedBinaryTree()

    assert tree.empty

    for key, data in test_single_threaded_tree:
        tree.insert(key=key, data=data)

    assert tree.empty is False
    assert list(tree.reverse_inorder_traverse()) == [(8, ''), (7, ''), (6, ''), (5, ''), (4, ''), (3, ''), (2, ''), (1, '')]
    tree.delete(1)
    assert tree.search(5).left.key == 4    
    assert tree.get_leftmost(node=tree.root).key == 2
    assert tree.get_rightmost(node=tree.root).key == 8
    assert tree.get_height(node=tree.root) == 3
    assert tree.get_predecessor(node=tree.root).key == 3
    temp = tree.search(key=5)
    assert tree.get_predecessor(node=temp).key == 4


def test_random_insert_delete_right():
    """Test random insert and delete."""
    for _ in range(0, 10):
        insert_data = random.sample(range(1, 2000), 1000)
        delete_data = random.sample(insert_data, 500)

        tree = single_threaded_binary_trees.RightThreadedBinaryTree()
        for key in insert_data:
            tree.insert(key=key, data=str(key))

        for key in delete_data:
            tree.delete(key=key)

        # we only care about the key of the traverse
        result = [item for item, _ in tree.inorder_traverse()]
        
        remaining_data = [item for item in insert_data if item not in delete_data]
        remaining_data.sort()  # sorts a list in ascending order
        assert result == remaining_data

def test_random_insert_delete_left():
    """Test random insert and delete."""
    for _ in range(0, 10):
        insert_data = random.sample(range(1, 2000), 1000)
        delete_data = random.sample(insert_data, 500)

        tree = single_threaded_binary_trees.LeftThreadedBinaryTree()
        for key in insert_data:
            tree.insert(key=key, data=str(key))

        # # debug
        # print("Before deleting:")
        # tree.root.display_keys(tree)
        
        for key in delete_data:
            tree.delete(key=key)
            
        # # debug
        # print(f"Deleted keys: {delete_data}")
        # print("After deleting: ")
        # tree.root.display_keys(tree)
        
        result_reverse = [item for item, _ in tree.reverse_inorder_traverse()]
        
        remaining_data = [item for item in insert_data if item not in delete_data]
        remaining_data.sort(reverse=True)  # sort a list in descending order
        
        # # debug
        # print(f"result: {result_reverse}")
        # print(f"remain: {remaining_data}")
        assert result_reverse == remaining_data