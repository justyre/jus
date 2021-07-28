# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Linked list implementation."""

from typing import Any


class Node:
    """Node in a linked list."""
    
    def __init__(self, data: Any) -> None:
        self.data = data
        self.next = None

class LinkedList:
    """Linked list."""
    
    def __init__(self) -> None:
        self.head = None
    
    def __len__(self):
        """Length of a linked list; 0 if empty. Usage like `len(linkedlist)`."""
        result = 0
        current = self.head
        while current is not None:
            result += 1
            current = current.next
        return result
    
    def __getitem__(self, position):
        """Get the element at `position` (starting from 0); if not found, return `None`.
        
        Usage like `linkedlist[2]`.
        """
        i = 0
        current = self.head
        while current is not None:
            if i == position:
                return current.data
            current = current.next
            i += 1
        return None
           
    def append(self, value: Any) -> None:
        """Append an item to the end of the linked list."""
        # `append` Node(value) to `self` by setting self.head.next to 
        # current_node & if current_node is None,  
        if self.head is None:
            self.head = Node(value)
        else:
            current_node = self.head
            while current_node.next is not None:
                current_node = current_node.next
            current_node.next = Node(value)
    
    def show_elements(self) -> None:
        """Show elements in a linked list."""
        current = self.head
        outlist = []
        while current is not None:
            outlist.append(current.data)
            current = current.next
        print(outlist)


# # the brute force method to make a linked list
# list1 = LinkedList()
# list1.head = Node(2)
# list1.head.next = Node(3)
# list1.head.next.next = Node(4)
# print(list1.head.next.next.data)

# make a linked list using `append` method defined in class
list2 = LinkedList()
list2.append(2)
list2.append(3)
list2.append(5)
list2.append(9)
print("length of list2: ", len(list2))
print("get element #2 (1st being #0): ", list2[2])
print("get element #11 (non-existent): ", list2[11])


# Reverse a linked list
#
# Check an example. To reverse (2,3,5) to (5,3,2), ie to change 
# `None.next = 2 = old list head, 2.next = 3, 3.next = 5, 5.next = None` to
# `None.next = 5 = new list head, 5.next = 3, 3.next = 2, 2.next = None`, 
# as Step1: set prev = None, current = 2, next_node = 3 = 2(current).next;
# Step2, do the reversion: set 2(current).next = None(prev);
# Step3, move one elem down the list --
# Notice that in order to use a while-loop, we need to move prev to 2(current)  
# and current to 3(next_node) for the iteration to move farther down the list.
# So now that prev & current have been moved, set next_node = 5 = current.next, 
# and do the `current.next = prev` again (ie 3.next = 2).
# It's obvious that what we need to loop over (ie put in the while-loop) is:
# `next_node = current.next; current.next = prev; prev = current; current = 
# next_node`. 
# Iterate till current is None, and prev is 5. Outside the loop, assign 5(prev) 
# as the new list head. The code is completedt.
def reverse_linked_list(list):
    """Reverse a linked list."""
    # for empty list, the reverse is empty, too
    if list.head is None:
        return
    
    current = list.head
    prev = None  
    while current is not None:
        # track the next node 
        next_node = current.next
        # modify the current node
        current.next = prev
        # update prev & current
        prev = current
        current = next_node
    
    list.head = prev

# show orig list2
list2.show_elements()
reverse_linked_list(list2)
# show reversed list2
list2.show_elements()