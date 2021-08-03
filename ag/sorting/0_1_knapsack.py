# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""0-1 knapsack problem."""

# Given n elements, each with (weight, profit), and determine the max profit that can be
# obtained by selecting a subset of the elements weighing <= capacity (capacity is a 
# predefined fixed integer).

from typing import Sequence
from tests import jovian

##########################################
### Test cases

tests = []

tests.append({
    'input': {
        'capacity': 165, 
        'weights': [23, 31, 29, 44, 53, 38, 63, 85, 89, 82],
        'profits': [92, 57, 49, 68, 60, 43, 67, 84, 87, 72]
    },
    'output': 309
})

# None of the elems can be included
tests.append({
    'input': {
        'capacity': 3,
        'weights': [4, 5, 6],
        'profits': [1, 2, 3]
    },
    'output': 0
})

# Only one elem can be included
tests.append({
    'input': {
        'capacity': 4,
        'weights': [4, 5, 1],
        'profits': [1, 2, 3]
    },
    'output': 3
})

# All elems can be included
tests.append({
    'input': {
        'capacity': 15,
        'weights': [4, 5, 6],
        'profits': [1, 2, 3]
    },
    'output': 6
})

# Multiple choices, choose the best
tests.append({
    'input': {
        'capacity': 15,
        'weights': [4, 5, 1, 3, 2, 5],
        'profits': [2, 3, 1, 5, 4, 7]
    },
    'output': 19
})

tests.append({
    'input': {
        'capacity': 170,
        'weights': [41, 50, 49, 59, 55, 57, 60],
        'profits': [442, 525, 511, 593, 546, 564, 617]
    },
    'output': 1735
})

##########################################
### Methods

def knapsack_recursive(capacity: int, weights: Sequence, profits: Sequence) -> float:
    """Solve 0-1 knapsack problem (maximize total profits) recursively."""
    # Time complexity: O(2^N)
    
    if len(weights) != len(profits):
        raise ValueError("weights and profits should be of the same length.")
    if not weights or not profits:
        return 0
    if weights[0] > capacity:
        return knapsack_recursive(capacity, weights[1:], profits[1:])
    else:
        return max(
            knapsack_recursive(capacity, weights[1:], profits[1:]),
            profits[0] + knapsack_recursive(capacity - weights[0], weights[1:], profits[1:])
        )

def knapsack_dynamic(capacity: int, weights: Sequence, profits: Sequence) -> float:
    """Solve 0-1 knapsack problem (maximize total profits) with dynamic programming."""
    # Time complexity: O(len(weights) * capacity)
    
    if len(weights) != len(profits):
        raise ValueError("weights and profits should be of the same length.")
    
    # table[i][j] is the max profit that can be obtained using the first i elems if the 
    # max capacity is j. table is of size (len(weights)+1) * (capacity+1).
    table = [[0] * (capacity + 1) for _ in range(len(weights) + 1)]
    for i in range(len(weights)):
        for j in range(capacity + 1):
            if weights[i] > j:
                table[i+1][j] = table[i][j]
            else:
                table[i+1][j] = max(table[i][j], profits[i] + table[i][j-weights[i]])
    return table[-1][-1]

##########################################
### Test client

# We can see that in small test cases, the running time of dynamic programming is even 
# longer than the brute-force recursive approach. This is different from the case in 
# common_subsequence.py, where the time saved by dynamic programming is immense
jovian.evaluate_test_cases_justyre(func=knapsack_recursive, tests=tests)
jovian.evaluate_test_cases_justyre(func=knapsack_dynamic, tests=tests)