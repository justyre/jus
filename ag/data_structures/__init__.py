"""Utilities and helper functions for algorithm learning."""

import textwrap, time

# string truncation:
# take `data` and only show the first `size` chars of it
def _str_trunc(data, size=100):
    data_str = str(data)
    if len(data_str) > size + 3:
        return data_str[:size] + '...'
    return data_str


# take `test_case` (dict) & show the input & expected output well-formatted
def _show_test_case(test_case):
    inputs = test_case['input']
    
    if 'outputs' in test_case:
        expected_text = "Outputs"
        # to get a value from a dict, we can use .get() or just []
        expected = test_case.get('outputs')
    else:
        expected_text = "Output"
        expected = test_case['output']
    
    # textwrap.dedent() trims all the COMMON leading whitespaces
    # for all lines of text in ()
    print(textwrap.dedent(
        """
        Input:
            {}
        
        Expected {}:
            {}
        """.format(_str_trunc(inputs), expected_text, _str_trunc(expected))
    ), end="")  # `end=""` changes the default ending `\n` of print() to `""`
    

# show the test result well-formatted
def _show_result(result):
    actual_output, passed, runtime = result
    pass_or_fail = "\033[92mPASSED!\033[0m" if passed else "\033[91mFAILED!\033[0m"
    print(textwrap.dedent(
        """
        Actual Output:
            {}
        
        Execution Time:
            {} microseconds
        
        Test Result:
            {}
        """.format(_str_trunc(actual_output), runtime, pass_or_fail)
    ))


def evaluate_test_case(func, test_case, display=True):
    """Evaluate one test case (as a dict).
    
    In other words, check if `func` works as expected for `test_case`.
    Set `display=False` if user decides not to see the input, expected and actual outputs.
    """
    inputs = test_case['input']
    
    if display:
        _show_test_case(test_case)
        
    timeStart = time.perf_counter_ns()
    # `**x` in python acts as a decompressor, ie taking all elems of x as inputs
    actual_output = func(**inputs)
    timeEnd = time.perf_counter_ns()
    # turn nanosec (1e-9) to microsec (1e-6) for better human readability
    runtime = (timeEnd - timeStart) / 1e3
    
    # if there are multiple expected outputs, reaching one of them is success
    if 'outputs' in test_case:
        passed = actual_output in test_case.get('outputs')
    else:
        passed = actual_output == test_case.get('output')
    
    result = actual_output, passed, runtime
    
    if display:
        _show_result(result)
    
    return result


def evaluate_test_cases(func, test_cases, error_only=True):
    """Evaluate multiple test cases (as a list of dicts).
    
    If `error_only=True`, will only display cases that fail.
    """
    results = []
    for i, test_case in enumerate(test_cases):
        result = evaluate_test_case(func, test_case, display=False)
        results.append(result)
        
        # we do nothing only when error_only=True AND this case has passed.
        # otherwise, we need to print out all the details
        if not (error_only and result[1]):
            print("\033[1mTest Case # {}:\033[0m".format(i))  # bold white
            _show_test_case(test_case)
            _show_result(result)
        
    total_cases = len(results)
    # python treats True as 1, False as 0
    num_passed = sum([r[1] for r in results])
    print("\033[1mSUMMARY OF TESTING {}\033[0m".format(func.__name__))
    print("Total Cases: {}, \033[92mPASSED\033[0m: {}, \033[91mFAILED\033[0m: {}".format(total_cases, num_passed, total_cases - num_passed))
    
    return results


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
        