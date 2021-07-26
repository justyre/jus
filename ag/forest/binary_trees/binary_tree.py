# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Abstract base class for generic binary trees.

Notes
-----
This module provides some custom types for type checking:
- `Pairs`: an iterator of Key-Value pairs. Yielded by traversal functions.

- `NodeType`: the type that any derived node class should upper-bound to.
"""

import abc

import dataclasses
from typing import Any, Generic, Iterator, Optional, Tuple, TypeVar

Pairs = Iterator[Tuple[Any, Any]]
"""An iterator of Key-Value pairs. Yielded by traversal functions."""


@dataclasses.dataclass
class Node:
    """Basic binary tree node definition."""
    
    # the `@dataclass` decorator will add the following methods automatically: 
    # __init__, __repr__, __eq__, __ne__, __lt__, __le__, __gt__, __ge__
    key: Any
    data: Any
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    parent: Optional["Node"] = None
    
    @abc.abstractmethod
    def display_keys(self, space: str = '\t', level: int = 0) -> None:
        """Display all the keys in a Node horizontally for clear visualization."""
        raise NotImplementedError()


NodeType = TypeVar("NodeType", bound=Node)
"""Type of a tree node that any derived node class should upper-bound to."""        

class BinaryTree(abc.ABC, Generic[NodeType]):
    """An abstract base class for any type of binary trees.
    
    This base class defines the basic properties and methods that all types of 
    binary trees should provide.
    
    Attributes
    ----------
    root: `Optional[NodeType]`
        The root node of the tree. The default is `None`.
    
    Notes
    -----
    One reason to use abstract base class (aka abc) for all types of binary trees 
    is to make sure that the types of different binary trees are compatible. Therefore, 
    binary tree traversals can be performed on any type of binary trees.
    """
    
    # `Generic[NodeType]` as a base class defines that the class `BinaryTree` takes a 
    # single "type parameter" NodeType. This also makes NodeType valid as a type within 
    # the class body.
    
    def __init__(self) -> None:
        self.root: Optional[NodeType] = None
    
    def __repr__(self) -> str:
        """Provide the tree representation to visualize its layout."""
        # Per Python document, this is to compute the official string representation 
        # of an object, which is typically used for debugging.
        if self.root:
            return (
                f"{type(self)}, root={self.root}, "
                f"tree_height={str(self.get_height(self.root))}"
            )
        return "Empty tree"
    
    @property
    def empty(self) -> bool:
        """bool: `True` if the tree is empty; `False` otherwise.
        
        Notes
        -----
        The property, `empty`, is read-only.
        Properties are not callable; when using, do as `if self.empty:`.
        """
        # If self.root is a Node (in red-black trees, this means it not being a Leaf), 
        # then the tree is not empty
        if isinstance(self.root, Node):
            return False
        return True
    
    @abc.abstractmethod    
    def search(self, key: Any) -> Optional[NodeType]:
        """Look for a node by a given key.
        
        Parameters
        ----------
        key: `Any`
            The key associated with the node.
        
        Returns
        -------
        `Optional[NodeType]`
            The node found by the given key.
        If the key does not exist, return `None`.
        
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def insert(self, key: Any, data: Any) -> None:
        """Insert a (key, data) pair into the binary search tree.
        
        Parameters
        ----------
        key: `Any`
            The key associated with the data.
        data: `Any`
            The data to be inserted.
        
        Raises
        ------
        `DuplicateKeyError`
            Raised if the key to be inserted already exists in the tree.
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def delete(self, key: Any) -> None:
        """Delete a node according to the given key.
        
        Parameters
        ----------
        key: `Any`
            The key of the node to be deleted.
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_leftmost(node: NodeType) -> NodeType:
        """Return the leftmost node from a given subtree.
        
        The key of the leftmost node is the smallest key in the given subtree.
        
        Parameters
        ----------
        node: `Node`
            The root of the subtree.
        
        Returns
        -------
        `Node`
            The node whose key is the smallest of the subtree of the given node.
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_rightmost(node: NodeType) -> NodeType:
        """Return the rightmost node from a given subtree.
        
        The key of the rightmost node is the largest key in the given subtree.
        
        Parameters
        ----------
        node: `Node`
            The root of the subtree.
        
        Returns
        -------
        `Node`
            The node whose key is the largest of the subtree of the given node.
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_predecessor(node: NodeType) -> Optional[NodeType]:
        """Return the predecessor in the in-order order.
        
        Parameters
        ----------
        node: `Node`
            The node to get its predecessor.
        
        Returns
        -------
        `Optional[NodeType]`
            The predecessor node.
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_successor(node: NodeType) -> Optional[NodeType]:
        """Return the successor in the in-order order.
        
        Parameters
        ----------
        node: `Node`
            The node to get its successor.
        
        Returns
        -------
        `Optional[Node]`
            The successor node.
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_height(node: Optional[NodeType]) -> int:
        """Get the height of the given subtree.
        
        Parameters
        ----------
        node: `Optional[NodeType]`
            The root of the subtree.
            
        Returns
        -------
        `int`
            The height of the given subtree. 
            0 if the subtree has only one node or is empty.
        """
        raise NotImplementedError()
