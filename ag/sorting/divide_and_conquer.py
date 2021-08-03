# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Several sorting implementation. Assume all input lists to be non-nested (ie flat)."""

import random
from typing import Callable, List, Optional, Sequence, Tuple

from tests import jovian

##########################################
### Test cases

tests = []

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


##########################################
### Methods

def bubble_sort(nums: Sequence) -> List:
    """Sort a list in non-descending order using bubble sort.
    
    Return a new list, leaving the original `nums` intact.
    """
    # Bubble sort compares each element with the next element, and if the previous one 
    # is greater than the next one, swap them. Repeat until the list is sorted.
    # Time complexity: O(N^2), space complexity: O(N).
    #
    # The inefficiency comes from the fact that we are shifting elements by AT MOST 
    # one position at a time.
    nums = nums.copy()
    for _ in range(len(nums) - 1):
        # Repeat the process, since we need to go back to the start again and again
        for i in range(len(nums) - 1):
            if nums[i] > nums[i + 1]:
                # Swap them
                nums[i], nums[i+1] = nums[i+1], nums[i]
    return nums

def insertion_sort(nums: Sequence) -> List:
    """Sort a list in non-descending order using insertion sort.
    
    Return a new list, leaving the original `nums` intact.
    """
    # Keep the initial portion sorted, and insert the remaining elems one by one at 
    # the right position.
    # Time complexity: O(N^2) (a little faster than bubble sort), space complexity: O(N)
    nums = nums.copy()
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
    nums: Sequence, has_display: bool = False, depth: int = 0
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
    nums: Sequence, has_display: bool = False, depth: int = 0
) -> List:
    # Solely for testing merge sort.
    return merge_sort(nums=nums, has_display=has_display, depth=depth)[1]

def _merge(
    nums1: Sequence, nums2: Sequence, has_display: bool = False, depth: int = 0
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
    nums: Sequence, k: int, has_display: bool = False, depth: int = 0
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
    lists: Sequence, has_display: bool = False, depth: int = 0
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

def quicksort(nums: Sequence, start: int = 0, end: Optional[int] = None) -> List:
    """Quicksort a list in non-descending order.
    
    Return a new list, leaving the original `nums` intact.
    """
    # # debugcode
    # print('quicksort', nums, start, end)
    # Time complexity: average case O(N log N), worst case O(N^2). Space: O(1).
    if end is None:
        # Only copy the list at the first step (ie only copy the initial list), 
        # to keep the original `nums` intact;
        # or the `nums` returned will be the same as the input `nums` forever
        nums = nums.copy()
        end = len(nums) - 1
    
    if start < end:
        pivot = _partition(nums, start, end)
        quicksort(nums, start, pivot - 1)
        quicksort(nums, pivot + 1, end)

    return nums

def _partition(li: Sequence, start: int = 0, end: Optional[int] = None) -> int:
    # Partition the list in-place, and return the position of the pivot element.
    # # debugcode
    # print('partition', li, start, end)
    if end is None:
        end = len(li) - 1
    
    left, right = start, end - 1
    while left < right:
        # # debugcode
        # print(' ', li, left, right)
        # We use the last elem as the pivot.
        if li[left] <= li[end]:
            # Increment left pointer if the elem <= pivot
            left += 1
        elif li[right] > li[end]:
            # Decrement right pointer if the elem > pivot
            right -= 1
        else:
            # Then li[left] > pivot AND li[right] <= pivot, so we swap them
            li[left], li[right] = li[right], li[left]
    
    # # debugcode
    # print(' ', li, left, right)
    # At this point, we must have left=right, ie the two pointers have overlapped
    if li[left] > li[end]:
        li[left], li[end] = li[end], li[left]
        return left
    else:
        return end

def quicksort_using_quickselect(nums: Sequence) -> List:
    """Quicksort non-descendingly using :py:meth:`sorting.divide_and_conquer.quickselect`.
    
    Return a new list, leaving the original `nums` intact.
    
    Note
    ----
    For large lists, this method is too slow to be feasible. This is only here to show one application of :py:meth:`sorting.divide_and_conquer.quickselect`.
    """
    nums = nums.copy()
    nums_sorted = []
    for i in range(len(nums)):
        # We don't care about the returned index of quickselect; we are only interested 
        # in the permutation quickselect() has brought about on `nums`.
        _ = quickselect(nums, 0, None, i)
        nums_sorted.append(nums[i])
    return nums_sorted

def quickselect(
    li: Sequence, left: int = 0, right: Optional[int] = None, n: int = 0
) -> int:
    """Return the index of such an element in the original `li`, as is the `n`'th element of this list when sorted non-descendingly (`n` starts from 0).
    
    Warning
    -------
    This function partially sorts the input `li`, so do back it up beforehand.
    """
    if right is None:
        right = len(li) - 1
    
    while True:
        if left >= right:
            return left
        pivot_index = _get_pivot_index(li, left, right)
        pivot_index = _trisection(li, left, right, pivot_index, n)
        if n == pivot_index:
            return n
        elif n < pivot_index:
            right = pivot_index - 1
        else:
            left = pivot_index + 1
            n -= pivot_index

def _get_pivot_index(li: Sequence, left: int, right: int) -> int:
    # Get the index of the median-of-medians of `li`, by dividing `li` into groups of 
    # <= 5 elems, 
    # and then computing the median of each group, then recursively compute the true 
    # median of the int(n/5) medians found in the previous step.
    # Note: this function calls quickselect(), so this is a mutual recursion.
    if right - left < 5:
        # For <= 5 elems, just get median
        return _median_of_less_than_five(li, left, right)
    
    for i in range(left, right, 5):
        # Each group is li[i:subright+1]
        subright = min(i + 4, right)
        median5 = _median_of_less_than_five(li, i, subright)
        # Move all median5's to the left of `li`, ie to li[l], li[l+1], etc
        # Note: double slash (//) is equivalent to int(). 
        # The difference: float//int returns float, while int(f/i) returns int.
        li[median5], li[left + (i-left)//5] = li[left + (i-left)//5], li[median5]
    
    # Now we have all the int(n/5) median5's in li[left:x]. We need to find the index 
    # of the mid'th largest number in this li[left:x], ie its median
    mid = int((right-left)/10) + left + 1
    return quickselect(li, left, left + int((right-left)/5), mid)

def _median_of_less_than_five(li: Sequence, left: int, right: int) -> int:
    # Return the index of the median of the ASC SORTED `li[left:right+1]` which is a 
    # group of at most five elems, using insertion sort.
    # Note: This function performs in-place sorting of li[l:r+1].
    i = left + 1
    while i <= right:
        j = i
        while j > left and li[j-1] > li[j]:
            li[j-1], li[j] = li[j], li[j-1]
            j -= 1
        i += 1
    return int((left + right) / 2)

def _trisection(li: Sequence, left: int, right: int, pivot_index: int, n: int) -> int:
    # Group li[left:right+1] into three parts: those < li[p_i], those = li[p_i], and 
    # those
    # > li[p_i], ie a three-way partition, and identify which part the n'th largest 
    # elem of the original `li` is in.
    # This ensures that the median-of-medians maintains linear execution time in a case 
    # of many all-coincident elems.
    
    pivot_value = li[pivot_index]
    # Move pivot elem to rightmost (temporarily, so that it will not be overwritten)
    li[pivot_index], li[right] = li[right], li[pivot_index]
    
    index_smaller = left
    for i in range(left, right):
        if li[i] < pivot_value:
            # Move all elems that < pivot to left of the pivot
            li[index_smaller], li[i] = li[i], li[index_smaller]
            index_smaller += 1
    
    index_equal = index_smaller
    for i in range(index_smaller, right):
        if li[i] == pivot_value:
            # Move all elems that = pivot right after the smaller elems
            li[index_equal], li[i] = li[i], li[index_equal]
            index_equal += 1
    
    # Move pivot to its final place, ie right after the equal elems (as last of them)
    li[index_equal], li[right] = li[right], li[index_equal]
    
    if n < index_smaller:
        # Then n'th largest elem should be in [0:index_smaller+1]
        return index_smaller
    if n <= index_equal:
        return n
    return index_equal


# Notebook class and custom comparisons

class Notebook:
    """Notebook class storing title, username, likes."""
    
    def __init__(self, title, username, likes) -> None:
        self.title = title
        self.username = username
        self.likes = likes
    
    def __repr__(self) -> str:
        """Representation of Notebook."""
        return f"Notebook <\"{self.username}/{self.title}\", {self.likes} likes>\n"

def bubble_sort_with_compare(nums: Sequence, compare: Callable[..., str]) -> List:
    """Bubble sort that accepts a custom comparison function.
    
    Return a new list, leaving the original `nums` intact.
    """
    nums = nums.copy()
    for _ in range(len(nums) - 1):
        # Repeat the process, since we need to go back to the start again and again
        for i in range(len(nums) - 1):
            if compare(nums[i], nums[i+1]) == 'greater':
                # Swap them
                nums[i], nums[i+1] = nums[i+1], nums[i]
    return nums

def insertion_sort_with_compare(nums: Sequence, compare: Callable[..., str]) -> List:
    """Perform insertion sort that accepts a custom comparison function.
    
    Return a new list, leaving the original `nums` intact.
    """
    nums = nums.copy()
    for i in range(1, len(nums)):
        # Note: the above line can use `for i in range(1,len(nums))` too, since for i=0,
        # the loop simply pops nums[0] out to cur and then put it back to [0], nothing.
        
        # list.pop(i) removes and returns the ith elem (starting with 0)
        current = nums.pop(i)
        j = i - 1
        while j >= 0 and compare(current, nums[j]) == 'lesser':
            j -= 1
        # When current >= nums[j], this is the place to be.
        # Note: list.insert(k) inserts BEFORE the kth elem
        nums.insert(j + 1, current)
        
    return nums

def merge_sort_with_compare(li: Sequence, compare: Callable[..., str]) -> List:
    """Merge sort that accepts a custom comparison function as the sorting criterion.
    
    Return a new list, leaving the original `nums` intact.
    """
    if len(li) < 2:
        return li
    mid = len(li) // 2
    return _merge_with_compare(
        merge_sort_with_compare(li[:mid], compare=compare),
        merge_sort_with_compare(li[mid:], compare=compare),
        compare
    )

def _merge_with_compare(left: Sequence, right: Sequence, compare: Callable[..., str]):
    # Similar to _merge(), but with a custom comparison func.
    i, j, merged = 0, 0, []
    while i < len(left) and j < len(right):
        compare_result = compare(left[i], right[j])
        if compare_result == 'lesser' or compare_result == 'equal':
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    return merged + left[i:] + right[j:]

def compare_likes_desc(nb1: Notebook, nb2: Notebook) -> str:
    """Compare the likes of two notebooks in descending order, ie the more the likes, the lesser the book gets."""
    if nb1.likes > nb2.likes:
        return 'lesser'
    elif nb1.likes == nb2.likes:
        return 'equal'
    else:
        return 'greater'

def compare_titles(nb1: Notebook, nb2: Notebook) -> str:
    """Compare the titles of two notebooks in alphabetical order."""
    if nb1.title < nb2.title:
        return 'lesser'
    elif nb1.title == nb2.title:
        return 'equal'
    else:
        return 'greater'

##########################################
### Test client

# Bubble sort, insertion sort

jovian.evaluate_test_cases(func=bubble_sort, test_cases=tests[:-1])
# jovian.evaluate_test_case(func=bubble_sort, test_case=tests[-1])
jovian.evaluate_test_cases(func=insertion_sort, test_cases=tests[:-1])
# jovian.evaluate_test_case(func=insertion_sort, test_case=tests[-1])

# Merge sort

print(merge_sort([5, -12, 2, 6, 1, 23, 7, 7, -12], has_display=True))
jovian.evaluate_test_cases(func=_merge_sort_for_testing, test_cases=tests)
# Next line shows that merge sort is much faster than bubble and insertion sort
# jovian.evaluate_test_case(func=_merge_sort_for_testing, test_case=tests[-1])

# k-way merge sort

k_way_merge_sort([5, -12, 2, 6, 1, 23, 7, 7, -12], k=4, has_display=True)

# Quicksort

jovian.evaluate_test_cases(func=quicksort, test_cases=tests)

# Quickselect

li = [3546, 1601, 8686, 4167, 649, 8931, 3233, 2292, 3822, 640, 7634, 8870, 7633, 6591, 3517]
print(quickselect(li, 0, None, 2), li, li[2])  # Should be 1601. li is partially sorted

# Quicksort using quickselect()

jovian.evaluate_test_cases(func=quicksort_using_quickselect, test_cases=tests[:-1])
# The next line takes too long to execute...although it will pass eventually.
# jovian.evaluate_test_case(func=quicksort_using_quickselect, test_case=tests[-1])


# Notebook and custom comparisons

nb = []
nb.append(Notebook('pytorch-basics', 'aakashns', 373))
nb.append(Notebook('linear-regression', 'siddhant', 532))
nb.append(Notebook('logistic-regression', 'vikas', 31))
nb.append(Notebook('feedforward-nn', 'sonaksh', 94))
nb.append(Notebook('cifar10-cnn', 'biraj', 2))
nb.append(Notebook('cifar10-resnet', 'tanya', 29))
nb.append(Notebook('anime-gans', 'hemanth', 80))
nb.append(Notebook('python-fundamentals', 'vishal', 136))
nb.append(Notebook('python-functions', 'aakashns', 74))
nb.append(Notebook('python-numpy', 'siddhant', 92))
print(nb)

nb_sorted = bubble_sort_with_compare(nb, compare=compare_likes_desc)
print('Result of bubble sort (like desc):')
print(nb_sorted)

nb_sorted2 = merge_sort_with_compare(nb, compare=compare_likes_desc)
print('Result of merge sort (like desc):')
print(nb_sorted2)

assert nb_sorted == nb_sorted2

nb_sorted = insertion_sort_with_compare(nb, compare=compare_titles)
print('Result of insertion sort (title asc):')
print(nb_sorted)

nb_sorted2 = merge_sort_with_compare(nb, compare=compare_titles)
print('Result of merge sort (title asc):')
print(nb_sorted2)

assert nb_sorted == nb_sorted2