"""Binary search algorithm implementation."""

from tests import jovian

##########################################
### Test cases

tests = []

# query occurs not as 1st or last elem
tests.append({
    'input': {
        'cards': [13, 11, 10, 7, 4, 3, 1, 0],
        'query': 7
    },
    'output': 3
})
tests.append({
    'input': {
        'cards': [13, 11, 10, 7, 4, 3, 1, 0],
        'query': 1
    },
    'output': 6    
})
        
# query is the 1st elem
tests.append({
    'input': {
        'cards': [4, 2, 1, -1],
        'query': 4
    },
    'output': 0
})            
 
# query is the last elem
tests.append({
    'input': {
        'cards': [3, -1, -9, -127],
        'query': -127
    },
    'output': 3
})

# cards contains just one elem
tests.append({
    'input': {
        'cards': [6],
        'query': 6
    },
    'output': 0
})

# if cards does not contain query, return -1
tests.append({
    'input': {
        'cards': [9, 7, 5, 2, -9],
        'query': 4
    },
    'output': -1
})

# cards is empty
tests.append({
    'input': {
        'cards': [],
        'query': 7
    },
    'output': -1
})

# cards have repeating numbers, but query is not repeated
tests.append({
    'input': {
        'cards': [8, 8, 6, 6, 6, 6, 6, 3, 2, 2, 2, 0, 0],
        'query': 3
    },
    'output': 7
})

# cards have repeating numbers, and query is repeated
# then return the first occurrence
tests.append({
    'input': {
        'cards': [8, 8, 6, 6, 6, 6, 6, 3, 2, 2, 2, 0, 0],
        'query': 6
    },
    'output': 2
})

# a large test case to compare time complexities
large_test = {
    'input': {
        'cards': list(range(int(1e7), 0, -1)),
        'query': 2
    },
    'output': int(1e7 - 2)
}

# a test case for first_and_last_position()
test_for_first_and_last = {
    'input': {
        'cards': [0, 0, 2, 2, 2, 3, 6, 6, 6, 6, 6, 8, 8],
        'query': 6
    },
    'output': (6, 10)
}

# test cases for count_rotations()
tests_for_rotations = []

# a list of size 10 rotated 3 times
tests_for_rotations.append({
    'input': {
        'nums': [19, 25, 29, 3, 5, 6, 7, 9, 11, 14]
    },
    'output': 3
})

# a list of size 8 rotated 5 times
tests_for_rotations.append({
    'input': {
        'nums': [11, 13, 17, 19, 23, 3, 5, 7]
    },
    'output': 5
})

# a list that was not rotated at all
tests_for_rotations.append({
    'input': {
        'nums': [1, 3, 5, 7, 9]
    },
    'output': 0
})

# a list that was rotated just once
tests_for_rotations.append({
    'input': {
        'nums': [9, 1, 3, 5, 7]
    },
    'output': 1
})

# a list that was rotated len(list)-1 times
tests_for_rotations.append({
    'input': {
        'nums': [3, 5, 7, 9, 1]
    },
    'output': 4
})

# an empty list
tests_for_rotations.append({
    'input': {
        'nums': []
    },
    'output': 0
})

# a one-elem list
tests_for_rotations.append({
    'input': {
        'nums': [5]
    },
    'output': 0
})

# contains repeating elems
tests_for_rotations.append({
    'input': {
        'nums': [5, 5, 6, 6, 6, 9, 9, 0, 0, 0, 2, 3, 3, 3, 3, 4, 4]
    },
    'output': 7
})


# test cases for locate_in_rotated_list_binary()
tests_for_locate_in_rotated_list = []

# a list of size 10 rotated 3 times
tests_for_locate_in_rotated_list.append({
    'input': {
        'nums': [19, 25, 29, 3, 5, 6, 7, 9, 11, 14],
        'target': 5
    },
    'output': 4
})

# an empty list
tests_for_locate_in_rotated_list.append({
    'input': {
        'nums': [],
        'target': 10
    },
    'output': -1
})

# a one-elem list
tests_for_locate_in_rotated_list.append({
    'input': {
        'nums': [5],
        'target': 10
    },
    'output': -1
})

# contains repeating elems
tests_for_locate_in_rotated_list.append({
    'input': {
        'nums': [5, 5, 6, 6, 6, 9, 9, 0, 0, 0, 2, 3, 3, 3, 3, 4, 4],
        'target': 3
    },
    'output': 11
})

###########################################
### Methods
# Input: cards(1 list, already sorted in desc order), query(1 num)
# Output: position of query in cards

def locate_card_linear(cards, query):
    """Linear search for `query` in a desc sorted list `cards`."""
    # time complexity: O(N)
    # space complexity: O(1)
    position = 0
    while position < len(cards):
                
        # check if current elem matches the query
        if cards[position] == query:
            return position
        position += 1
        
    # if we have reached the end of the list w/out returning, 
    # then query is not in cards
    return -1


# method 2: binary search for `query` in a desc sorted list `cards`

def binary_search(lo, hi, condition):
    """Binary search."""
    # time complexity: O(log N)
    # space complexity: O(1)
    # dep: condition()

    # keep looping as long as the substring exists
    while lo <= hi:
        mid = (lo + hi) // 2  # the int division
        result = condition(mid)        

        if result == 'found':
            return mid
        elif result == 'left':
            hi = mid - 1  # move `hi` (thus next `mid`) to the left
        elif result == 'right':
            lo = mid + 1  # move to the right
    
    # if nothing is returned, nothing is found
    return -1   
    
def locate_card_binary(cards, query):
    """Binary search for `query` in a desc sorted list `cards`."""
    def condition(mid):
        # helper inner func: 
        # decides where to look for `query` in `cards` given position `mid`
        # time complexity: O(1)
        # note: this is an inner func, so it can access the variables within
        # the outer func (eg. cards, query)
        if cards[mid] == query:
            # even if we've found the matching value, it may not be leftmost!
            if mid > 0 and cards[mid - 1] == query:
                # there are repeating elems, so move to the left
                return 'left'
            else:
                # no repeating elems exist, ie we've found it!
                return 'found'
        elif cards[mid] < query:
            return 'left'  # cards is descending
        else:
            return 'right'
    
    # do the binary search
    return binary_search(0, len(cards) - 1, condition)

def first_position(cards, query):
    """Find the first position of `query` in `cards` which is already asc sorted."""
    # Similar to locate_card_binary().
    # If nothing is found, returns -1
    def condition(mid):
        if cards[mid] == query:
            if mid > 0 and cards[mid - 1] == query:
                return 'left'
            return 'found'  # `else` is not essential, coz prev `if` returned
        elif cards[mid] < query:
            return 'right'  # cards is asc
        else:
            return 'left'
        
    # do the binary search
    return binary_search(0, len(cards) - 1, condition)

def last_position(cards, query):
    """Find the last position of `query` in `cards` which is already asc sorted."""
    def condition(mid):
        if cards[mid] == query:
            if mid < len(cards) - 1 and cards[mid + 1] == query:
                return 'right'
            return 'found'
        elif cards[mid] < query:
            return 'right'
        else:
            return 'left'
        
    # do the binary search
    return binary_search(0, len(cards) - 1, condition)

def first_and_last_position(cards, query):
    """Find both the first & last position of `query` in `cards`."""
    return first_position(cards, query), last_position(cards, query)

def count_rotations_linear(nums):
    """Rotate an asc sorted list `rotations` times to get the list `nums`."""
    # Rotating a list is defined as removing the last elem of the list & 
    # adding it before the 1st elem, eg [3,2,4,1] -> [1,3,2,4].
    # 
    # since the orig list is sorted asc, after k rotations, the orig [0]
    # (smallest) is now at [k], and it's the only elem who has a bigger 
    # predecessor. thus, we simply need to check for each elem whether it <
    # its predecessor (if there is one), and the answer is simply k. if
    # no such elem exists, k must be 0 (not rotated at all).
    # time complexity: O(N)
    position = 1
    while position < len(nums):
        if position > 0 and nums[position - 1] > nums[position]:
            return position
        # otherwise, move a step rightwards
        position += 1
        
    # if nothing is returned, then the whole `nums` is asc or empty, 
    # ie not rotated at all, so return 0
    return 0

def count_rotations_binary(nums):
    """Binary search approach to `count_rotations_linear()`."""
    # if the mid elem < its predecessor, ans = mid; otherwise,
    # if the mid elem < last elem of the substring, ans is left of mid,
    # coz [ans] < [ans+1] < .. < [last] < [0] < [1] < .. < [ans-1],
    # and it's obvious that mid is in [ans, last-1], ie ans < mid;
    # similarly, if [mid] > [last], mid must be in [0,ans-1], ie ans>mid.
    # time complexity: O(log N)
    lo, hi = 0, len(nums) - 1
    # Note: when nums is empty, hi = -1 < lo = 0, does not go into while-loop
    while lo <= hi:
        mid = (lo + hi) // 2  # int division
        if mid > 0 and nums[mid] < nums[mid - 1]:
            return mid
        elif nums[mid] < nums[-1]:
            hi = mid - 1
        else:
            lo = mid + 1
    
    # if nothing is returned, nums is asc or empty, needs 0 rotation
    return 0

def count_rotations_using_binary_search(nums):
    """Rotate an asc sorted list `rotations` times to get the list `nums`, using `binary_search()`."""
    def condition(mid):
        if mid > 0 and nums[mid] < nums[mid - 1]:
            return 'found'
        elif nums[mid] < nums[-1]:
            return 'left'
        else:
            return 'right'
    
    # do the binary search, but for cases that return -1, adjust to 0
    return max(0, binary_search(0, len(nums) - 1, condition))

def locate_in_rotated_list_binary(nums, target):
    """Search for `target`'s first position in a rotated list `nums`."""
    # nums is not sorted, so we'll have to find the position of [0]
    # in the orig list in `nums`. Then we'll turn `nums` 
    # back to the orig list `nums_asc`, and we'll find target's position
    # in nums_asc, say [k], by binary or linear search. Now target is at position
    # `k+ans` % len(nums) (ie if k+ans > len(nums), subtract len(nums)).
    # time complexity: O(log N)

    # find the position of [0] in the orig asc list in `nums`
    smallest = count_rotations_binary(nums)
    # turn `nums` back to the orig asc list `nums_asc`.
    # this also works for an empty `nums` coz list(range(0)) is empty
    nums_asc = [nums[(k + smallest) % len(nums)] for k in range(len(nums))]
    # find where `target` is in `nums_asc`.
    # note: locate_card_binary() is only for DESC sorted lists
    target_pos = first_position(nums_asc, target)
    
    # if `nums` is an empty list or if `target` cannot be found, return -1
    if len(nums) == 0 or target_pos == -1:
        return -1
    # else, return the result
    return (target_pos + smallest) % len(nums)
        

##################################
### Test client

jovian.evaluate_test_cases_justyre(locate_card_binary, tests)

print("\nJovian style:\n")
jovian.evaluate_test_cases(locate_card_binary, tests)
# jovian.evaluate_test_case(locate_card_linear, large_test)
# jovian.evaluate_test_case(locate_card_binary, large_test)
jovian.evaluate_test_case(first_and_last_position, test_for_first_and_last)
jovian.evaluate_test_cases(count_rotations_linear, tests_for_rotations)
jovian.evaluate_test_cases(count_rotations_binary, tests_for_rotations)
jovian.evaluate_test_cases(count_rotations_using_binary_search, tests_for_rotations)

jovian.evaluate_test_cases(locate_in_rotated_list_binary, tests_for_locate_in_rotated_list)
# evaluate_test_cases(locate_in_rotated_list_binary, tests_for_locate_in_rotated_list)