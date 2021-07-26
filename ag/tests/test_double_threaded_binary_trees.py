"""Unit tests for the single threaded binary search tree module."""

import random

from forest.binary_trees import double_threaded_binary_trees


def test_double_threaded_tree(test_single_threaded_tree: list) -> None:
    """Test the basic opeartions of a binary search tree."""
    tree = double_threaded_binary_trees.DoubleThreadedBinaryTree()

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
    
def test_random_insert_delete_both():
    """Test random insert and delete."""
    for _ in range(0, 10):
        insert_data = random.sample(range(1, 2000), 1000)
        delete_data = random.sample(insert_data, 500)

        tree = double_threaded_binary_trees.DoubleThreadedBinaryTree()
        for key in insert_data:
            tree.insert(key=key, data=str(key))

        for key in delete_data:
            tree.delete(key=key)

        # we only care about the key of the traverse
        result = [item for item, _ in tree.inorder_traverse()]
        result_reverse = [item for item, _ in tree.reverse_inorder_traverse()]
        
        remaining_data = [item for item in insert_data if item not in delete_data]
        remaining_data.sort()  # sorts a list in ascending order
        assert result == remaining_data
        remaining_data.sort(reverse=True)
        assert result_reverse == remaining_data