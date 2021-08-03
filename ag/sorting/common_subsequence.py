# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Longest common subsequence. The subsequence does not need to be continuous in the original sequence."""

from typing import Sequence, Tuple
from tests import jovian

import functools

##########################################
### Test cases

tests = []

# List
tests.append({
    'input': {
        'seq1': [1, 3, 5, 6, 7, 2, 5, 2, 3],
        'seq2': [6, 2, 4, 7, 1, 5, 6, 2, 3]
    },
    'output': ([1, 5, 6, 2, 3], 5)
})

# Tuple
tests.append({
    'input': {
        'seq1': (1, 3, 5, 6, 7, 2, 5, 2, 3),
        'seq2': (6, 2, 4, 7, 1, 5, 6, 2, 3)
    },
    'output': ((1, 5, 6, 2, 3), 5)
})

# String
tests.append({
    'input': {
        'seq1': 'serendipitous',
        'seq2': 'precipitation'
    },
    'output': ('reipito', 7)
})

# One is a subseq of the other
tests.append({
    'input': {
        'seq1': 'dense',
        'seq2': 'condensed'
    },
    'output': ('dense', 5)
})

# Multiple subseqs with same length
# In this case, return the first common subseq (the first from the left of seq1).
tests.append({
    'input': {
        'seq1': 'abcdef',
        'seq2': 'badcfe'
    },
    'output': ('ace', 3)
})

# No common subseq
tests.append({
    'input': {
        'seq1': 'a',
        'seq2': 'bb'
    },
    'output': ('', 0)
})

# One is empty
tests.append({
    'input': {
        'seq1': '',
        'seq2': 'stone'
    },
    'output': ('', 0)
})

##########################################
### Methods

def memoize(obj):
    """Cache a function's return value each time it is called. If called later with the same arguments, the cached value is directly returned rather than reevaluated."""
    # Initialize cache and obj.cache as an empty dict
    cache = obj.cache = {}
    
    # The decorator 'wraps' will run `functools.partial(update_wrapper, wrapped=obj)`, 
    # ie `update_wrapper(wrapper=memoizer, wrapped=obj)`. (wrapped is the orig func, 
    # while wrapper is the func to be updated.) So obj's attributes will be copied to 
    # memoizer. memoizer() is returned as the replacement for the orig `obj`
    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            # When args are not present in cache's keys, add them
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer

# The decorator 'memoize' will go and execute function `memoize(lcs)`, return memoizer.
# Without memoization, the orig func runs too slow (impossible when len(seq) > 7)
@memoize
def lcs_recursive(seq1: Sequence, seq2: Sequence) -> Tuple[Sequence, int]:
    """Find the longest common subsequence (both itself and its length) of two sequences recursively.
    
    Note
    ----
    If there are multiple subseqs with same length, return the first common subseq from the left of `seq1`.
    """
    # Time complexity: O(2 ^ (len(seq1) + len(seq2)))
    if type(seq1) != type(seq2):
        raise TypeError("Both input sequences should be of the same type.")
    
    # Consider all subclasses of generic type `Sequence`
    if isinstance(seq1, list):
        empty = []
    elif isinstance(seq1, str):
        empty = ''
    elif isinstance(seq1, tuple):
        empty = ()
    else:
        raise TypeError("This type of sequence is not supported; try list, str, tuple.")
    if not seq1 or not seq2:
        # If any one of the seqs is empty, then return the empty seq-type
        return empty, 0

    if seq1[0] == seq2[0]:
        if isinstance(seq1, list):
            add_elem = [seq1[0]]
        elif isinstance(seq1, str):
            add_elem = seq1[0]
        elif isinstance(seq1, tuple):
            # A one-elem tuple can only be shown as (3,) but not (3)
            add_elem = (seq1[0],)
        return (
            add_elem + lcs_recursive(seq1[1:], seq2[1:])[0],
            1 + lcs_recursive(seq1[1:], seq2[1:])[1]
        )
    else:
        # max(s1, s2, key=len) means to get from s1, s2 the one with bigger len()
        return (
            max(lcs_recursive(seq1, seq2[1:])[0], lcs_recursive(seq1[1:], seq2)[0], key=len),
            max(lcs_recursive(seq1, seq2[1:])[1], lcs_recursive(seq1[1:], seq2)[1])
        )

def lcs_dynamic(seq1: Sequence, seq2: Sequence) -> int:
    """Find the longest common subsequence (both itself and its length) of two sequences by dynamic programming.
    
    Note
    ----
    If there are multiple subseqs with same length, return the first common subseq from the left of `seq1`.
    """
    # Time complexity: O(len1 * len2). Space complexity: O(len1 * len2).
    
    # Step 1: find the lcs's length
    
    if type(seq1) != type(seq2):
        raise TypeError("Both input sequences should be of the same type.")

    # Consider all subclasses of generic type `Sequence`
    if isinstance(seq1, list):
        empty = []
    elif isinstance(seq1, str):
        empty = ''
    elif isinstance(seq1, tuple):
        empty = ()
    else:
        raise TypeError("This type of sequence is not supported; try list, str, tuple.")
    if not seq1 or not seq2:
        # If any one of the seqs is empty, then return the empty seq-type
        return empty, 0
    
    len1, len2 = len(seq1), len(seq2)
    # Use nested lists to make a (len1+1) * (len2+1) 2D array (ie a table).
    # table[i][j] is the lcs length of seq1[0:i] and seq2[0:j]
    table = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            # We start from range(1,) since seq[0:0] is empty, so its lcs w/any seq is 0
            if seq1[i - 1] == seq2[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])
    # The next two lines are equivalent; use either
    # lcs_length = table[len1][len2]
    lcs_length = table[-1][-1]
    
    # Step 2: find the lcs ITSELF
    
    lcs = empty
    
    # Note: The vital idea here is, now that we know the length of lcs to be index, 
    # ie the elem at the lower right corner of `table`, we should travel from it 
    # BACKWARDS (ie going up and right `table`) to find the feasible lcs.
    i, j = len1, len2
    while i > 0 and j > 0:
        if seq1[i-1] == seq2[j-1]:
            if isinstance(seq1, list):
                add_elem = [seq1[i-1]]
            elif isinstance(seq1, str):
                add_elem = seq1[i-1]
            elif isinstance(seq1, tuple):
                # A one-elem tuple can only be shown as (3,) but not (3)
                add_elem = (seq1[i-1],)
            lcs = add_elem + lcs
            i -= 1
            j -= 1
        elif table[i-1][j] < table[i][j-1]:
            # If the current elem of seq1 & seq2 are not the same, then find the larger 
            # of the two predecessors and go in that direction (ie in search of lcs).
            # Note: Putting this `elif <` first is important; if we swap this elif with 
            # the next `else`, the resulting lcs will be the 1st common subseq from the 
            # left of seq2, instead of the left of seq1.
            j -= 1
        else:
            i -= 1

    return lcs, lcs_length


##########################################
### Test client

jovian.evaluate_test_cases(func=lcs_recursive, test_cases=tests)
# From the next two tests, we can see that memoized recursion is faster than plain-
# vanilla dynamic programming
jovian.evaluate_test_cases_justyre(func=lcs_recursive, tests=tests)
jovian.evaluate_test_cases_justyre(func=lcs_dynamic, tests=tests)