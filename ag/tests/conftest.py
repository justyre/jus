"""Common test data for pytest."""

import pytest


@pytest.fixture
def basic_tree() -> list:
    """Return tree data for building a basic test tree."""
    return [
        (23, "23"),
        (4, "4"),
        (30, "30"),
        (11, "11"),
        (7, "7"),
        (34, "34"),
        (20, "20"),
        (24, "24"),
        (22, "22"),
        (15, "15"),
        (1, "1"),
    ]

@pytest.fixture
def test_tree_inorder_postorder() -> list:
    """Return tree data for building a test tree for inorder & postorder traversals."""
    return [
        (5, ""),
        (6, "4"),
        (3, "30"),
        (4, "11"),
        (2, "7"),
        (1, "34"),
    ]

@pytest.fixture
def test_tree_reverse_inorder() -> list:
    """Return tree data for building a test tree for reverse inorder traversals."""
    return [
        (2, ""),
        (1, "4"),
        (4, "30"),
        (3, "11"),
        (5, "7"),
        (6, "34"),       
    ]

@pytest.fixture
def test_single_threaded_tree() -> list:
    """Return tree data for building a test single threaded tree."""
    return [
        (4, ""),
        (1, ""),
        (7, ""),
        (3, ""),
        (5, ""),
        (8, ""),
        (2, ""), 
        (6, ""),       
    ]    