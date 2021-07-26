# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Sorting implementation."""

import random
from typing import List, Tuple

from tests import jovian

##########################################
### Test cases

tests: List = []

# List of numbers in random order
tests.append({
    'input': {
        'nums': [5, 2, 6, 1, 23, 7, -12, 12, -243, 0]
    },
    'output': [-243, -12, 0, 1, 2, 5, 6, 7, 12, 23]
})

# List with repeating elements
tests.append({
    'input': {
        'nums': [4, 2, 6, 3, 4, 6, 2, 1]
    },
    'output': [1, 2, 2, 3, 4, 4, 6, 6]
})

tests.append({
    'input': {
        'nums': [42, 42, 42, 42, 42, 42, 42]
    },
    'output': [42, 42, 42, 42, 42, 42, 42]
})

# A list that is already sorted
tests.append({
    'input': {
        'nums': [3, 5, 6, 8, 9, 10, 99]
    },
    'output': [3, 5, 6, 8, 9, 10, 99]
})

# A list that is sorted in descending order
tests.append({
    'input': {
        'nums': [99, 10, 9, 8, 6, 5, 3]
    },
    'output': [3, 5, 6, 8, 9, 10, 99]
})

# An empty list
tests.append({
    'input': {
        'nums': []
    },
    'output': []
})

# A list with just one element
tests.append({
    'input': {
        'nums': [23]
    },
    'output': [23]
})

# A randomized list
in_list = list(range(10000))
out_list = list(range(10000))
random.shuffle(in_list)
tests.append({
    'input': {
        'nums': in_list
    },
    'output': out_list
})


###########################################
### Methods

def bubble_sort(nums: List) -> List:
    """Sort a list in non-descending order using bubble sort in-place."""
    # Bubble sort compares each element with the next element, and if the previous one 
    # is greater than the next one, swap them. Repeat until the list is sorted.
    # Time complexity: O(N^2), space complexity: O(N).
    #
    # The inefficiency comes from the fact that we are shifting elements by AT MOST 
    # one position at a time.
    for _ in range(len(nums) - 1):
        # Repeat the process, since we need to go back to the start again and again
        for i in range(len(nums) - 1):
            if nums[i] > nums[i + 1]:
                # Swap them
                nums[i], nums[i+1] = nums[i+1], nums[i]
    return nums

def insertion_sort(nums: List) -> List:
    """Sort a list in non-descending order using insertion sort in-place."""
    # Keep the initial portion sorted, and insert the remaining elems one by one at 
    # the right position.
    # Time complexity: O(N^2) (a little faster than bubble sort), space complexity: O(N)
    for i in range(len(nums)):
        # Note: the above line can use `for i in range(1,len(nums))` too, since for i=0,
        # the loop simply pops nums[0] out to cur and then put it back to [0], nothing.
        
        # list.pop(i) removes and returns the ith elem
        current = nums.pop(i)
        j = i - 1
        while j >= 0 and current < nums[j]:
            j -= 1
        # When current >= nums[j], this is the place to be.
        # Note: list.insert(k) inserts BEFORE the kth elem
        nums.insert(j + 1, current)
    return nums

def merge_sort(
    nums: List, has_display: bool = False, depth: int = 0
) -> Tuple[int, List]:
    """Sort a list in non-descending order using merge sort.
    
    Return a new list, leaving the original `nums` intact.
    Meanwhile, count all the inversions in the list.
    If `has_display=True`, print some info to show the recursion process.
    """
    # Two elems a[i], a[j] form an inversion if i<j and a[i]>a[j].
    # Time complexity: O(N log N). Space complexity: O(N).
    if has_display:
        print('  ' * depth, 'merge_sort:', nums)
    
    inversion_count = 0    
    if len(nums) <= 1:
        # Terminating condition (one-elem list has no inversions)
        return (inversion_count, nums)
    
    mid = len(nums) // 2
    # Split nums into two halves
    left_nums = nums[:mid]
    right_nums = nums[mid:]
    
    # Sort for each half recursively
    new_inversions, left_sorted = merge_sort(left_nums, has_display, depth+1)
    inversion_count += new_inversions
    new_inversions, right_sorted = merge_sort(right_nums, has_display, depth+1)
    inversion_count += new_inversions
    
    # Combine the two sorted halves into one
    new_inversions, nums_sorted = _merge(
        left_sorted, right_sorted, has_display, depth+1
    )
    inversion_count += new_inversions
    return inversion_count, nums_sorted

def _merge_sort_for_testing(
    nums: List, has_display: bool = False, depth: int = 0
) -> List:
    # Solely for testing merge sort.
    return merge_sort(nums=nums, has_display=has_display, depth=depth)[1]

def _merge(
    nums1: List, nums2: List, has_display: bool = False, depth: int = 0
) -> Tuple[int, List]:
    # Merge two sorted lists into one sorted list (non-descending).
    # If has_display is True, print some info to show the recursion process.
    # Meanwhile, count new inversions incurred during merging.
    # Time complexity: O(N), where N=len(nums1)+len(nums2).
    merged = []
    # Indices for iteration
    i, j = 0, 0
    inversion_count = 0
    
    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            # Include the smaller element in merged, and move to the next elem
            merged.append(nums1[i])
            i += 1
        else:
            # At any step in _merge(), if nums1[i]>nums2[j], since nums1 is asc sorted, 
            # all the remaining elems in nums1 (nums1[i+1, .., len-1]) will be greater 
            # than nums2[j], ie. inversion count increases by len(nums1)-i.
            merged.append(nums2[j])
            inversion_count += len(nums1) - i
            j += 1
    # Attach the remaining elems to merged. Recall that both nums1&2 are sorted
    merged = merged + nums1[i:] + nums2[j:]
    if has_display:
        print('  ' * depth, '_merge:', nums1, nums2, 'into', merged)
    return inversion_count, merged

def k_way_merge_sort(
    nums: List, k: int, has_display: bool = False, depth: int = 0
) -> List:
    """Sort a list in non-descending order using k-way merge sort.
    
    Return a new list, leaving the original `nums` intact.
    If `has_display=True`, print some info to show the recursion process.
    """
    # Per Wikipedia, we implement iterative 2-way merge by iteratively merging 
    # the two shortest sublists.
    # Time complexity: O(N log k) (note that k < n). Space complexity: O(N).
    if has_display:
        print('  ' * depth, 'k_way_merge_sort:', nums)
        
    if len(nums) <= 1:
        # Terminating condition
        return nums
    
    # Split nums into k sublists
    sublists = []
    sublist_length = max(len(nums) // k, 1)
    for i in range(0, len(nums), sublist_length):
        sublist = nums[i : i + sublist_length]
        # Sort for each sublist recursively
        sublist_sorted = k_way_merge_sort(sublist, k, has_display, depth+1)
        sublists.append(sublist_sorted)
    # Combine the k sorted sublists into one
    nums_sorted = _k_way_merge(sublists, has_display, depth+1)
    return nums_sorted

def _k_way_merge(
    lists: List, has_display: bool = False, depth: int = 0
) -> List:
    # Merge a list of sorted lists (`lists`) into one sorted list (non-descending).
    # If has_display is True, print some info to show the recursion process.
    # Time complexity: O(N), where N=len(nums1)+len(nums2).
    while len(lists) >= 2:
        sizes_of_sublists = [len(list) for list in lists]
        # When there are at least two lists to merge...
        # Find the shortest list and pop it
        for index, list in enumerate(lists):
            if len(list) == min(sizes_of_sublists):
                shortest_list = lists.pop(index)
                sizes_of_sublists.pop(index)
                break
        # Find the second shortest list and pop it
        for index, list in enumerate(lists):
            if len(list) == min(sizes_of_sublists):
                second_shortest_list = lists.pop(index)
                sizes_of_sublists.pop(index)
                break
            
        # merge the two
        _, two_merged = _merge(
            shortest_list, second_shortest_list, has_display, depth+1
        )
        lists.append(two_merged)
    
    # The only elem in `lists` is the sorted list
    return lists[0]


##################################
### Test client

# bubble sort, insertion sort

jovian.evaluate_test_cases(func=bubble_sort, test_cases=tests[:-1])
# jovian.evaluate_test_case(func=bubble_sort, test_case=tests[-1])
jovian.evaluate_test_cases(func=insertion_sort, test_cases=tests[:-1])
# jovian.evaluate_test_case(func=insertion_sort, test_case=tests[-1])

# merge sort

print(merge_sort([5, -12, 2, 6, 1, 23, 7, 7, -12], has_display=True))
jovian.evaluate_test_cases(func=_merge_sort_for_testing, test_cases=tests)
# Next line shows that merge sort is much faster than bubble and insertion sort
# jovian.evaluate_test_case(func=_merge_sort_for_testing, test_case=tests[-1])

# k-way merge sort

k_way_merge_sort([5, -12, 2, 6, 1, 23, 7, 7, -12], k=4, has_display=True)

# testing: count inversions