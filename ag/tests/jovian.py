# Licensed under MIT License. Courtesy of Jovian.
# See LICENSE in the project root for license information.

"""Testing utilities and helper functions for algorithm learning."""

from typing import Any, Callable, Iterable, Mapping, Sequence, Union
import pytest
import textwrap
import time

def evaluate_test_case(
    func: Callable, test_case: Mapping, has_display: bool = True, 
    extra_func_kwargs: Mapping = {}
) -> str:
    """Evaluate one test case (as a dict), ie check if `func` works as expected for `test_case`.
    
    Set `has_display=False` if user decides not to see the input, expected and actual outputs.
    
    Note
    ----
    Pass extra `kwargs` for `func` through `extra_func_kwargs` as a dict or another type of `Mapping`.
    """
    inputs = test_case['input']
    
    if has_display:
        _show_test_case(test_case)
        
    timeStart = time.perf_counter_ns()
    # `**x` in python acts as a decompressor, ie taking all elems of x as inputs
    actual_output = func(**inputs, **extra_func_kwargs)
    timeEnd = time.perf_counter_ns()
    # turn nanosec (1e-9) to microsec (1e-6) for better human readability
    runtime = (timeEnd - timeStart) / 1e3
    
    # Check if output is nested, since pytest.approx() cannot deal with nested structure
    try:
        # If there are multiple expected outputs, reaching one of them is success
        if 'outputs' in test_case:
            passed = pytest.approx(actual_output) in test_case.get('outputs')
        else:
            passed = pytest.approx(actual_output) == test_case.get('output')
    except TypeError:
        # Catch the TypeError about pytest not being able to deal with nested 
        # structures. The treatment is to flatten them into non-nested lists
        print("Output is nested; flattening...")
        actual_output = list(flatten(actual_output))
        if 'outputs' in test_case:
            outputs = [list(flatten(item)) for item in test_case.get('outputs')]
            passed = pytest.approx(actual_output) in outputs
        else:
            output = list(flatten(test_case.get('output')))
            passed = pytest.approx(actual_output) == output  
    
    result = actual_output, passed, runtime
    
    if has_display:
        _show_result(result)
    
    return result

def evaluate_test_cases(
    func: Callable, test_cases: Sequence[Mapping], is_error_only: bool = True,
    extra_func_kwargs: Mapping = {}
) -> str:
    """Evaluate multiple test cases (as a list of dicts).
    
    If `is_error_only=True`, will only has_display cases that fail.
    
    Note
    ----
    Pass extra `kwargs` for `func` through `extra_func_kwargs` as a dict or another type of `Mapping`.
    """
    print()
    results = []
    for i, test_case in enumerate(test_cases):
        result = evaluate_test_case(func, test_case, has_display=False, extra_func_kwargs=extra_func_kwargs)
        results.append(result)
        
        # we do nothing only when is_error_only=True AND this case has passed.
        # otherwise, we need to print out all the details
        if not (is_error_only and result[1]):
            print("\033[1mTest Case # {}:\033[0m".format(i))  # bold white
            _show_test_case(test_case)
            _show_result(result)
        
    total_cases = len(results)
    # python treats True as 1, False as 0
    num_passed = sum([r[1] for r in results])
    print("\033[1mSUMMARY OF TESTING {}, with extra kwargs: {}\033[0m".format(func.__name__, extra_func_kwargs if extra_func_kwargs else 'None'))
    print("Total Cases: {}, \033[92mPASSED\033[0m: {}, \033[91mFAILED\033[0m: {}".format(total_cases, num_passed, total_cases - num_passed))
    
    return results


def evaluate_test_cases_justyre(
    func: Callable, tests: Union[Mapping, Sequence], extra_func_kwargs: Mapping = {}
) -> None:
    """Evaluate multiple test cases (as a list of dicts).
    
    See Also
    --------
    :py:meth:`tests.jovian.evaluate_test_cases`. These two methods provide the same 
    information in slightly different formats. Besides, this function does not provide a switch to show error cases only; for that, use `evaluate_test_cases()`.
    """    
    print()
    print("\033[1mTESTING {}, with extra kwargs: {}\033[0m".format(func.__name__, extra_func_kwargs if extra_func_kwargs else 'None'))
    # if `tests` is not a list(ie it is a dict), turn it into one
    if not isinstance(tests, list):
        tests = [tests]
        
    for i, test in enumerate(tests):
        expected_output = test['output']
        time_start = time.perf_counter_ns()
        actual_output = func(**test['input'], **extra_func_kwargs)
        time_end = time.perf_counter_ns()
        print("\033[1mTest Case # {}:\033[0m".format(i))  # bold white
        # Check if output is nested, since pytest.approx() cannot deal with it
        try:
            passed = expected_output == pytest.approx(actual_output)
        except TypeError:
            # Catch the TypeError about pytest not being able to deal with nested 
            # structures. The treatment is to flatten them into non-nested lists
            print("Output is nested; flattening...")
            fla_actual_output = list(flatten(actual_output))
            fla_expected_output = list(flatten(expected_output))
            passed = fla_expected_output == pytest.approx(fla_actual_output)
        
        if passed:
            print("Test \033[92mPASSED!\033[0m")
        else:
            print("Test \033[91mFAILED!\033[0m")
        print("---------------------")
        print("Expected Output:", expected_output)
        print("Actual Output:", actual_output)
        print("Execution Time (includes sleep):", time_end - time_start, "ns\n")

def flatten(s):
    """Flatten a nested list or tuple."""
    for elem in s:
        if isinstance(elem, Iterable) and not isinstance(elem, (str, bytes)):
            yield from flatten(elem)
        else:
            yield elem

def _str_trunc(data: Any, size: int = 100) -> str:
    # String truncation:
    # Take `data` and only show the first `size` chars of it
    data_str = str(data)
    if len(data_str) > size + 3:
        return data_str[:size] + '...'
    return data_str

def _show_test_case(test_case: Mapping) -> None:
    # Take `test_case` (dict) & show the input & expected output well-formatted
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

def _show_result(result: str) -> None:
    # Show the test result well-formatted
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