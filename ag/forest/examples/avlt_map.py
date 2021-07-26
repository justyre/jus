"""Implement a Map using an AVL binary search tree."""

from typing import Any, Optional
from forest.binary_trees import avl_tree
from forest.binary_trees import traversal

class Map:
    """Key-value Map implemented using AVL Tree."""
    
    def __init__(self) -> None:
        self._avlt = avl_tree.AVLTree()
        
    def __setitem__(self, key: Any, value: Any) -> None:
        """Insert (key, value) item into the map."""
        self._avlt.insert(key=key, data=value)
    
    def __getitem__(self, key: Any) -> Optional[Any]:
        """Get the data by the given key. Return `None` if not found."""
        node = self._avlt.search(key=key)
        if node:
            return node.data
        return None
    
    def __delitem__(self, key: Any) -> None:
        """Remove a (key, value) pair from the map."""
        self._avlt.delete(key=key)
        
    def __iter__(self) -> traversal.Pairs:
        """Iterate through all the data in the map in-order."""
        return traversal.inorder_traverse(tree=self._avlt)
    
    @property
    def empty(self) -> bool:
        """Return `True` if the Map is empty; `False` otherwise."""
        return self._avlt.empty


if __name__ == "__main__":
    
    # Initialize the Map instance
    contacts = Map()
    
    # Add some items
    contacts["Mark"] = "mark@email.com"
    contacts["Luke"] = "luke@email.com"
    contacts["Wendy"] = "wendy@email.com"
    contacts["John"] = "john@email.com"
    
    # Retrieve a data
    print(contacts["Luke"])
    
    # Delete an item
    del contacts["Luke"]
    
    # Check the deleted item; should be None
    print(contacts["Luke"])
    
    # Iterate the items
    for contact in contacts:
        print(contact)
        
    # Another way of iteration
    print(list(contacts))