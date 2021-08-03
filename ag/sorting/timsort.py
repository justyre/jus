# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Timsort implementation."""

# This algorithm finds subsequences that are already ordered (called "runs") and uses 
# them to sort the remainder more efficiently. It is a hybrid of insertion sort and 
# merge sort, taking advantage of the merits of both sorting techniques.
# For a detailed introduction, cf.
# https://svn.python.org/projects/python/trunk/Objects/listsort.txt
# The complete C implementation code of this algorithm in Python source can be found:
# https://hg.python.org/cpython/file/tip/Objects/listobject.c

from typing import List, Sequence

import copy
import random
    
def find_minrun(n: int) -> int:
    """Compute a good value for the minimum run length.
    
    Natural runs shorter than this are boosted artificially via binary insertion.
    """
    r = 0  # Becomes 1 if any bits are shifted off
    assert n >= 0
    while n >= 64:
        # The target of this while-loop:
        # If n is an exact power of 2, return 32;
        # otherwise, return int k in [32,64] such that n/k is close to, but strictly 
        # less than, an exact power of 2 that is larger than 2^1=2.
        
        # | is `OR by bits`, & is `AND by bits`. ie r = r|(n&1).
        # The next two lines of code work as follows:
        # 1. If n is an exact power of 2, then for all loops, n&1=0, r=r|0=0|0=0, 
        # and n is halved, until n=64 and is halved to 32, with r=0, so returns 32.
        # 2. Otherwise, then there must be at least one `1` among the second to the 
        # last digits of n's binary form, eg.10010000. We scan from the rightmost digit # to the left, and whenever a 1 is met, r is 1. n will decrease to the n//2^k 
        # that is closest to but less than 64. The target is met.
        #
        # In essence, this procedure is simply taking the first 6 bits of n, and add 
        # 1 if any of the remaining bits is 1 (we call a bit that is 1 a "set bit").

        r |= n & 1
        n >>= 1  # move n's binary form all 1 digit to the right, ie n = n // 2
    # If n < 64, just return n, since it is too small to bother with fancy stuff
    return n + r

def insertion_sort(li: Sequence, left: int, right: int) -> List:
    """Sort [left, right) of a list in non-decreasing order using insertion sort in-place."""
    # Keep the initial portion sorted, and insert the remaining elems one by one at 
    # the right position.
    # Time complexity: O(N^2) (a little faster than bubble sort), space complexity: O(N)
    for i in range(left+1, right):
        # list.pop(i) removes and returns the ith elem
        current = li[i]
        j = i - 1
        while j >= left and current < li[j]:
            li[j+1] = li[j]
            j -= 1
        # When current >= nums[j], this is the place to be.
        # Note: list.insert(k) inserts BEFORE the kth elem
        li[j+1] = current

def merge(li: Sequence, left_index: int, mid_index: int, right_index: int) -> None:
    """Merge two sorted sublists into one sorted list in-place.
    
    The two sorted sublists are: `li[l:m]`, `li[m:r]`.
    """
    left_li = li[left_index : mid_index]
    right_li = li[mid_index : right_index]
    i, j, k = 0, 0, left_index
    
    while i < len(left_li) and j < len(right_li):
        if left_li[i] <= right_li[j]:
            li[k] = left_li[i]
            i += 1
        else:
            li[k] = right_li[j]
            j += 1
        k += 1
    
    # Copy the remainders
    while i < len(left_li):
        li[k] = left_li[i]
        i += 1
        k += 1
    while j < len(right_li):
        li[k] = right_li[j]
        j += 1
        k += 1

def tim_sort(li: Sequence) -> List:
    """Tim sort a list and return a new list, leaving the original one intact."""
    minrun = find_minrun(len(li))
    
    for start in range(0, len(li), minrun):
        # Note that insertion_sort sorts [left, right)
        end = min(start + minrun, len(li))
        insertion_sort(li, start, end)
    
    size = minrun
    while size < len(li):
        for left in range(0, len(li), 2 * size):
            # Since [left : left+size] and [left+size : left+2*size] have been sorted 
            # (when size=minrun, these two have been sorted by insertion_sort; when 
            # size is doubled, they are sorted by the previous loop), we can use merge.
            mid = min(left + size, len(li))
            right = min(left + 2 * size, len(li))
            merge(li, left, mid, right)
        size *= 2

def _count_run(li: Sequence, lo: int, hi: int) -> int:
    """Count the length of the run beginning at lo, in the slice [lo, hi).
    
    lo < hi is required on entry.
    """
    # "A run" is either the longest non-decreasing sequence, or the longest strictly 
    # decreasing sequence. `descending` is False in the former case, True in the latter.
    # Note: This function is not required by tim_sort(), so we make it internal.
    assert lo < hi
    # descending = False
    lo += 1
    if lo == hi:
        return 1
    
    n = 2  # run count
    if li[lo] < li[lo-1]:
        # descending = True
        for lo in range(lo+1, hi):
            if li[lo] >= li[lo-1]:
                break
            n += 1
    else:
        for lo in range(lo+1, hi):
            if li[lo] < li[lo-1]:
                break
            n += 1
    
    return n


#########################
# Driver code

sample_list = random.sample(range(1, 2000), 1000)
# sample_list = [-1,5,0,-3,11,9,-2,7,0]
print("Count run:", _count_run(sample_list, lo=1, hi=len(sample_list)))

# Note: in the next line, using `orig = sample_list` won't work (orig will be changed).
# This is because we don't have two lists; this assignment just copies the REFERENCE to 
# sample_list, not the actual list object. Use li.copy() or list(li) instead.
orig_sample = sample_list.copy()
# orig_sample = list(sample_list)
tim_sort(sample_list)

# Note: sorted() is not in-place; it produces a new list, leaving the original intact
sorted_by_python = sorted(sample_list)
assert sample_list == sorted_by_python


# Demonstrate that only copy.deepcopy() is totally reliable.
# For an non-nested list, use li.copy() or list(li). For a nested list (that has lists as its elems), we can only use `import copy; copy.deepcopy(li)` to do copying properly.

sample_list = [[-1,5,0],-3,11,9,-2,7,0]
copied = {}
copied['.copy()'] = sample_list.copy()
copied['list()'] = list(sample_list)
copied['*1'] = sample_list * 1
copied['copy.copy()'] = copy.copy(sample_list)
copied['copy.deepcopy()'] = copy.deepcopy(sample_list)

sample_list[0].append(11)
print("Sample:", sample_list)
print("Copied:")
# Note that dict.items() is only an iterator for dict
[print(key, ":", value) for key, value in copied.items()]