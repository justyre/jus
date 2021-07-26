"""Implement ordered index using double threaded binary search trees."""

from typing import Any
from forest.binary_trees import double_threaded_binary_trees
from forest.binary_trees import traversal

class MyDatabase:
    """Example using double threaded BST to build an index.
    
    Useful when space complexity is concerned and the specific traversals are critical.
    """
    
    def __init__(self) -> None:
        self._double_bst = double_threaded_binary_trees.DoubleThreadedBinaryTree()
        
    def _persist(self, payload: Any) -> str:
        """Fake function pretending to store some data to file system.
        
        Parameters
        ----------
        payload: Any
            Any data.
        
        Returns
        -------
        str
            Path to the payload.
        """
        return f"path_to_{payload}"
    
    def insert_data(self, key: Any, payload: Any) -> None:
        """Insert data.
        
        Parameters
        ----------
        key: Any
            Unique key for the payload.
        payload: Any
            Any data.
        """
        path = self._persist(payload=payload)
        self._double_bst.insert(key=key, data=path)
        
    def dump(self, ascending: bool = True) -> traversal.Pairs:
        """Dump the data in an ascending or descending order.
        
        Parameters
        ----------
        ascending: bool
            The desired order of data output.
            
        Yields
        ------
        `Pairs`
            The next (key, data) pair.
        """
        if ascending:
            return self._double_bst.inorder_traverse()
        return self._double_bst.reverse_inorder_traverse()
    

if __name__ == "__main__":
    
    # Initialize the database
    my_database = MyDatabase()
    
    # Add some items
    my_database.insert_data("Adam", "Adam is a boy")
    my_database.insert_data("Betty", "Betty is a girl")
    my_database.insert_data("Peter", "Peter is naughty")
    my_database.insert_data("David", "David is peaceful")
    
    # Dump the items in a certain order
    print("Ascending:")
    for contact in my_database.dump():
        print(contact)
    
    print("Descending:")
    print(list(my_database.dump(ascending=False)))
    