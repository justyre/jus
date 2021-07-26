# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Hash table implementation assuming none of the keys is None."""

from typing import Any, Generator, List, Optional

import random
import textwrap

class HashTable:
    """Hash table using linear probing."""
    
    # Suppose that none of the key of any item in the hash table is empty (ie None).
    def __init__(self) -> None:
        self._n: int = 0  # number of elements
        # Default capacity of the hash table (ie max elems it can hold) 
        self._capacity: int = 1
        self._list: List = [None] * self._capacity        
    
    def __len__(self):
        """Total number of non-empty key-value pairs in the hash table.
        
        With this, we can get the total by `len(hashtable)`.
        """
        # Note: This is len(self), not len(self._list).
        # Actually, `len(self._list) == self._capacity` always holds.
        return self._n
    
    def __getitem__(self, key: Any) -> Optional[Any]:
        """Find the value associated with a key.
        
        With this, we can get an element by [''].
        """
        index = self.get_valid_index(_list=self._list, key=key)
        pair = self._list[index]
        # Return the value of the pair if found, else return None
        return None if pair is None else pair[1]
    
    def __setitem__(self, key: Any, value: Any) -> None:
        """Insert a new key-value pair.
        
        With this, we can set an element's value by ['']. 
        If it doesn't exist, we insert it; if it already exists, we update it.
        """
        if self._n == self._capacity:
            # We are out of space, so resize by doubling the capacity.
            self._resize(capacity=2 * self._capacity)
            
        index = self.get_valid_index(_list=self._list, key=key)
        pair = self._list[index]
        if (pair is None) or (pair == (None, None)) or (pair[0] != key):
            # pair is the old elem in _list. If pair was empty, surely size increments;
            # if pair's key was different from the new key, it's an insertion, not an 
            # update, so size increments, too
            self._n += 1
        self._list[index] = (key, value)
        
    def __iter__(self) -> Generator[Any, None, Any]:
        """Iterate over all key-value pairs.
        
        With this, we can iterate by `for key, value in hashtable:` (in ascending order)
        """
        # A generator can be annotated by the generic type 
        # Generator[YieldType, SendType, ReturnType].
        for pair in self._list:
            if pair is not None and pair != (None, None):
                yield pair
        # ANOTHER IMPLEMENTATION USING LIST COMPREHENSION
        # Note: The following `return` cannot be changed to `yield`!
        # return (pair for pair in self._list if pair is not None and pair != (None, None))
    
    def __delitem__(self, key: Any) -> None:
        """Delete a key-value pair from the hash table."""
        index = self.get_valid_index(_list=self._list, key=key)
        pair = self._list[index]
        if (pair is not None) and (pair != (None, None)) and (pair[0] == key):
            # Set the elem to be a tombstone.
            # Note: `(None, None)` is different from `None`
            self._list[index] = (None, None)
            # pair is the old elem in _list. If pair's key was the same as the new key, 
            # it's a valid deletion, so size decrements
            self._n -= 1
            if self._n < self._capacity // 4:
                # If the number of elems drops below one quarter of capacity, 
                # shrink the capacity by half
                self._resize(capacity=self._capacity // 2)
    
    def __repr__(self) -> str:
        """Represent all key-value pairs."""
        pairs = [textwrap.indent(f"{repr(pair[0])} : {repr(pair[1])}", '  ') for pair in self if pair is not None and pair != (None, None)]
        # Use str.join() to get the desired string output
        return "{\n" + ',\n'.join(pairs) + "\n}"
    
    def __str__(self) -> str:
        """Represent all key-value pairs."""
        return repr(self)
    
    def display_keys(self) -> List:
        """Display all the keys."""
        display_list: List = []
        for pair in self._list:
            if pair is not None and pair != (None, None):
                display_list.append(pair[0])
        return display_list
        # ANOTHER IMPLEMENTATION USING LIST COMPREHENSION
        # return [pair[0] for pair in self._list if pair is not None and pair != (None, None)]
                   
    @staticmethod
    def get_valid_index(_list: List, key: Any) -> int:
        """Get the valid hash index for a key."""
        # Use Python's in-built `hash` function:
        # Equal objects have equal hash value; but the reverse is not necessarily true.
        index = hash(key) % len(_list)
        while True:
            # Implement linear probing to avoid collision between diff keys w/same hash
            pair = _list[index]
            # If pair is empty or a tombstone, or the stored key matches the given key, 
            # then this is the right place, so return the index
            if (pair is None) or (pair == (None, None)) or (pair[0] == key):
                return index
            # Otherwise, move on to the next index
            index += 1
            # If we have reached the end of the list, go back to the start
            if index == len(_list):
                index = 0
    
    def _resize(self, capacity: int) -> None:
        # Dynamic resizing of the hash table to `capacity`.
        # In the f-string below, `5,d` means fieldwidth 5 and comma for a thousands sep.
        print(f"Hash table has {self._n:5,d} elements; resizing to a capacity of {capacity:5,d}.")
        new_list = [None] * capacity
        for index in range(self._capacity):
            if self._list[index] != (None, None) and self._list[index] is not None:
                # We don't need any empty elems in the `new_list`.
                # We need to find the `new_index` for each elem in `new_list`
                new_index = self.get_valid_index(
                    _list=new_list, key=self._list[index][0]
                )
                # Copy existing elems to the `new_index` places
                new_list[new_index] = self._list[index]
        # Update self's attributes
        self._list = new_list
        self._capacity = capacity


class HashTableSeparateChaining():
    """Hash table using separate chaining with Python lists as buckets."""
    
    def __init__(self) -> None:
        self._n: int = 0  # number of elements, aka size of hashtable (counting no None)
        self._capacity: int = 1
        self._table: List = [None] * self._capacity
    
    def __len__(self):
        """Total number of non-empty key-value pairs in the hash table.
        
        With this, we can get the total by `len(hashtable)`.
        """
        # Note: This is len(self), not len(self._table).
        # Actually, `len(self._table) == self._capacity` always holds.
        return self._n
    
    def __getitem__(self, key: Any) -> Optional[Any]:
        """Find the key-value pair associated with a key.
        
        With this, we can get an element by `hashtable[key]`.
        """
        index = self.get_valid_index(key=key, capacity=self._capacity)
        bucket = self._table[index]
        if bucket is None:
            # If the bucket with `index` is empty, the key does not exist
            return None
        for pair in bucket:
            if pair[0] == key:
                return pair[1]
        # If the bucket with `index` exists, but none of the elems in bucket matches key
        return None
    
    def __setitem__(self, key: Any, value: Any) -> None:
        """Insert a new key-value pair.
        
        With this, we can set an element's value by `hashtable[key]`. 
        If it doesn't exist, we insert it; if it already exists, we update it.
        """
        if self._n == self._capacity:
            # We are out of space, so resize by doubling the capacity.
            self._resize(capacity=2 * self._capacity)
            
        index = self.get_valid_index(key=key, capacity=self._capacity)
        if self._table[index] is None:
            self._table[index] = []
        for pair_pos, pair in enumerate(self._table[index]):
            if pair[0] == key:
                # Update
                self._table[index][pair_pos] = (key, value)
                return
        # If none of the elems in bucket `index` has key `key`, it is an insertion
        self._table[index].append((key, value))
        self._n += 1
    
    def __iter__(self) -> Generator[Any, None, Any]:
        """Iterate over all key-value pairs.
        
        With this, we can iterate by `for key, value in hashtable:` (in ascending order)
        """
        # A generator can be annotated by the generic type 
        # Generator[YieldType, SendType, ReturnType].
        for index in range(self._capacity):
            if self._table[index] is not None:
                for pair in self._table[index]:
                    if pair != (None, None):
                        yield index, pair
    
    def __delitem__(self, key: Any) -> None:
        """Delete a key-value pair from the hash table."""
        index = self.get_valid_index(key=key, capacity=self._capacity)
        if self._table[index] is not None:
            for pair_pos, pair in enumerate(self._table[index]):
                if pair[0] == key:
                    # Valid deletion. Set the elem to be a tombstone.
                    # Note: `(None, None)` is different from `None`
                    self._table[index][pair_pos] = (None, None)
                    self._n -= 1
                    if self._n < self._capacity // 4:
                        # If the number of elems drops below one quarter of capacity, 
                        # shrink the capacity by half
                        self._resize(capacity=self._capacity // 2)
    
    def __repr__(self) -> str:
        """Represent all key-value pairs."""
        # Note: the following `for pair in self` uses self.__iter__()
        pairs = [textwrap.indent(f"{repr(pair[0])} : {repr(pair[1])}", '  ') for _, pair in self if pair is not None and pair != (None, None)]
        # Use str.join() to get the desired string output
        return "{\n" + ',\n'.join(pairs) + "\n}"
    
    def __str__(self) -> str:
        """Represent all key-value pairs."""
        return repr(self)
    
    def display_keys(self) -> List:
        """Display all the keys."""
        display_list: List = []
        for _, pair in self:
            if pair is not None and pair != (None, None):
                display_list.append(pair[0])
        return display_list            
    
    def get_valid_index(self, key: Any, capacity: int) -> int:
        """Get the valid hash index for a key."""
        # Use Python's in-built `hash` function:
        # Equal objects have equal hash value; but the reverse is not necessarily true.
        for original_index, pair in self:
            if pair[0] == key:
                # When `key` already exists in the hash table, we need to find the 
                # original index of the existing `key` in the hash table, instead of 
                # creating a new index (Note: Python's hash() is non-consistent).
                if original_index <= capacity:
                    return original_index
                else:
                    # This will happen when the new capacity is smaller (ie a shrink).
                    # Then we need to find an empty place to put the original_index.
                    # This is always possible, since capacity is the number of buckets, 
                    # and per self.__delitem__(), we only shrink to half capacity when 
                    # the number of elems in self < capacity // 4.
                    for index in range(capacity):
                        if self._table[index] is None:
                            return index
        # If key `key` does not exist in the table, we can assign a new index to it
        return hash(key) % capacity
    
    def _resize(self, capacity: int) -> None:
        # Dynamic resizing of the hash table to `capacity`.
        # In the f-string below, `5,d` means fieldwidth 5 and comma for a thousands sep.
        print(f"Hash table has {self._n:5,d} elements; resizing to a capacity of {capacity:5,d}.")
        new_table = [None] * capacity

        for _, pair in self:
            # By design of self.__iter__(), we don't have any empty or tomb `pair` here.
            # We need to find the `new_index` for each elem in the old table
            new_index = self.get_valid_index(key=pair[0], capacity=capacity)
            if new_table[new_index] is None:
                # Note: [] is not None (although [] evaluates to False)
                    new_table[new_index] = []
            new_table[new_index].append(pair)            
                    
        # Update self's attributes
        self._table = new_table
        self._capacity = capacity
        
        
    
                

# test client

if __name__ == "__main__":
    
    # Test HashTable
    
    print("\nTesting HashTable...\n")
    table = HashTable()
    print(table, len(table), list(table), table.display_keys(), table._list)
    # Insert with setitem magic method
    # Meanwhile, check the handling of different keys with the same letter combination
    table['listen'] = 1
    table['silent'] = 34
    assert table['listen'] == 1 and table['silent'] == 34
    print(table, len(table))

    # Update with setitem
    table['listen'] = 99
    print(table, len(table))
    assert table['listen'] == 99 and table['silent'] == 34

    assert len(table) == 2

    # Get a list of key-value pairs, which invokes iter magic method
    # Note: the list is not necessarily sorted asc by key, since hash(key) changes randomly
    print(table.display_keys())
    print(list(table))
    print(table)

    # Next line is equivalent to: table.__delitem__('listen')
    del table['listen']
    print(table.display_keys())
    print(list(table))
    print(table, len(table))

    table['listen'] = 5
    print(table, len(table))

    table['a'] = 7
    print(table, len(table))
    
    # Random test
    
    table = HashTable()
    print("Inserting 1,000 elements to the hash table...")
    for j in range(1000):
        table[j] = random.randint(0,9)
    print("Done.\n")
    
    print(f"len(table) = {len(table)}")
    print(f"len(table._list) = {len(table._list)}, table._capacity = {table._capacity}")
    
    print("Deleting 995 elements from the hash table...")
    for j in range(995):
        del table[j]
    print(table._list, len(table), len(table._list))
    print(table)
    print(table.display_keys())
    
    print(list(table.__iter__()))
    
    
    
    # Test HashTableSeparateChaining
    
    print("\nTesting HashTableSeparateChaining...\n")
    table = HashTableSeparateChaining()
    print(table, len(table), list(table), table.display_keys(), table._table)
    # Insert with setitem magic method
    # Meanwhile, check the handling of different keys with the same letter combination
    table['listen'] = 1
    table['silent'] = 34
    # assert table['listen'] == 1 and table['silent'] == 34
    print(table, len(table), table._table)

    # Update with setitem
    table['listen'] = 99
    print(table, len(table), table._table, table['listen'], table['silent'])
    assert table['listen'] == 99 and table['silent'] == 34
    
    table['green'] = 67
    print(table, len(table), table._table)
    assert len(table) == 3

    # Get a list of key-value pairs, which invokes iter magic method
    # Note: the list is not necessarily sorted asc by key, since hash(key) changes randomly
    print(table.display_keys())
    print(list(table))
    print(table)

    # Next line is equivalent to: table.__delitem__('listen')
    del table['listen']
    print(table.display_keys())
    print(list(table))
    print(table, len(table), table._table)

    table['listen'] = 5
    print(table, len(table), table._table)

    table['a'] = 7
    print(table, len(table), table._table)
    
    table['listen'] = 23
    print(table, len(table), table._table)

    # Random test
    
    table = HashTableSeparateChaining()
    print("Inserting 1,000 elements to the hash table...")
    for j in range(1000):
        table[j] = random.randint(0,9)
    print("Done.\n")
    
    print(f"len(table) = {len(table)}")
    print(f"len(table._table) = {len(table._table)}, table._capacity = {table._capacity}")
    
    print("Deleting 995 elements from the hash table...")
    for j in range(995):
        del table[j]
    print(table._table, len(table), len(table._table))
    print(table)
    print(table.display_keys())
    
    print(list(table.__iter__()))