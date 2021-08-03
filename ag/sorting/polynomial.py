# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Univariate polynomial multiplications.

The input polynomials can be sorted in either ascending or descending power-of-term order, but all the polynomials should be sorted in the same order.
"""

import cmath
import math
from typing import List, Sequence

from tests import jovian

##########################################
### Test cases

tests = []

tests.append({
    'input': {
        'poly1': [7, 5, 0, 2],
        'poly2': [2, 4, 3]
    },
    'output': [14, 38, 41, 19, 8, 6]
})

tests.append({
    'input': {
        'poly1': [7],
        'poly2': [2, 4, 3]
    },
    'output': [14, 28, 21]
})

tests.append({
    'input': {
        'poly1': [1, 1, 0],
        'poly2': [1, -1, 0]
    },
    'output': [1, 0, -1, 0, 0]
})

# An empty input list should be treated as [0]
tests.append({
    'input': {
        'poly1': [7, 5, 0, 2],
        'poly2': []
    },
    'output': [0]
})

tests.append({
    'input': {
        'poly1': [],
        'poly2': []
    },
    'output': [0]
})

##########################################
### Methods

def poly_multiply_basic(poly1: Sequence, poly2: Sequence) -> List:
    """Multiply two univariate polynomials using direct brute-force approach."""
    # Time complexity: Theta(N^2).
    # Actually, the convolution of the vectors (a0,a1,..,an) and (b0,b1,..,bm),
    # (c0,c1,..,c(m+n)), is defined as: c[k] = sum_{i=0}^{k} (a[i]*b[k-i]).
    
    if not poly1 or not poly2:
        # If either is an empty list, return [0]
        return [0]
    
    result = [0] * (len(poly1) + len(poly2) - 1)
    for k in range(len(result)):
        for i in range(len(poly1)):
            if i <= k and i < len(poly1) and k - i < len(poly2):
                result[k] += poly1[i] * poly2[k - i]
    return result

def poly_multiply_fft(
    poly1: Sequence, poly2: Sequence, method: str = 'iterative'
) -> List:
    """Multiply two univariate polynomials using discrete FFT approach.
    
    The kwarg `method` (type `str`) can be set to either `recursive` or `iterative`, invoking the respective implementation of discrete FFT.
    """
    # Time complexity: Theta(N log N), since both fft and inverse_fft cost 
    # Theta(N log N), and the bridging pointwise multiplication only costs Theta(N).
    
    if not poly1 or not poly2:
        # If either is an empty list, return [0]
        return [0]
    
    # First, we need to pad poly1&2 with 0's to make both have a length of 2^t.
    max_length = max(len(poly1), len(poly2))
    new_length = 2 ** (1 + math.ceil(math.log2(max_length)))
    padded_poly1 = poly1 + [0] * (new_length - len(poly1))
    padded_poly2 = poly2 + [0] * (new_length - len(poly2))
    
    # Step 1: Evaluation (coef form -> point-value form)
    if method == 'recursive':
        ffted_poly1 = fft_recursive(padded_poly1)
        ffted_poly2 = fft_recursive(padded_poly2)
    elif method == 'iterative':
        ffted_poly1 = fft_iterative(padded_poly1)
        ffted_poly2 = fft_iterative(padded_poly2)
    else:
        raise ValueError("kwarg `method` can only be 'recursive' or 'iterative'.")
    
    # Step 2: Pointwise multiplication (p-v -> p-v)
    ffted_product = [val1 * val2 for val1, val2 in zip(ffted_poly1, ffted_poly2)]
    
    # Step 3: Interpolation (p-v form -> coef form)
    inverse_ffted_product = inverse_fft_recursive(ffted_product)
    
    # Discard the excessive trailing 0's, since len(result) should be len1+len2-1
    result = inverse_ffted_product[:(len(poly1) + len(poly2) - 1)]
    return result

def fft_recursive(poly: Sequence) -> List:
    """Recursive discrete fast Fourier transform (DFT) of a polynomial with a degree that is `2^t-1`, t being a positive integer (ie `len(poly)` should be an exact power of 2).
    
    Input is coeffcient form, output is point-value form (values are complex numbers).
    """
    # For algo detail, cf. CLRS Ch30.2.
    # Time complexity: Theta(N log N)
    
    n = len(poly)
    if n == 1:
        return poly
    
    even_subpoly = [item for index, item in enumerate(poly) if index % 2 == 0]
    odd_subpoly = [item for index, item in enumerate(poly) if index % 2 != 0]
    # Note: To mark the imaginary part in Python, use `*1j` (1 cannot be omitted)
    principal_root_of_unity = cmath.exp((2 * cmath.pi / n) * 1j)
    omega = 1  # this is principal root (aka omega_n) raised to the power of 0
    
    even_out = fft_recursive(even_subpoly)
    odd_out = fft_recursive(odd_subpoly)
    out = [0] * n
    for k in range(n//2):
        # Note: poly(x) = even_subpoly(x^2) + x * odd_subpoly(x^2).
        # Here we evaluate poly(x) at n points: omega_n^0, omega_n^1, .., omega_n^(n-1).
        out[k] = even_out[k] + omega * odd_out[k]
        out[k + n//2] = even_out[k] - omega * odd_out[k]
        omega *= principal_root_of_unity
        
    return out

def inverse_fft_recursive(
    poly: Sequence, has_imaginary: bool = False, imag_threshold: float = 1e-14
) -> List:
    """Recursive inverse discrete fast Fourier transform of a descending polynomial with a degree that is `2^t-1`, t being a positive integer.
    
    Input is point-value form, output is coefficient form.
    """
    # For algo detail, cf. CLRS Ch30.2.
    # Time complexity: Theta(N log N)
    
    n = len(poly)
    if n == 1:
        return poly
    
    even_subpoly = [item for index, item in enumerate(poly) if index % 2 == 0]
    odd_subpoly = [item for index, item in enumerate(poly) if index % 2 != 0]
    # Note: To mark the imaginary part in Python, use `*1j` (1 cannot be omitted)
    principal_root_of_unity = cmath.exp(-(2 * cmath.pi / n) * 1j)
    omega = 1  # this is principal root (aka omega_n) raised to the power of 0
    
    even_out = inverse_fft_recursive(even_subpoly)
    odd_out = inverse_fft_recursive(odd_subpoly)
    out = [0] * n
    for k in range(n//2):
        # Note: poly(x) = even_subpoly(x^2) + x * odd_subpoly(x^2).
        # Here we evaluate poly(x) at n points: omega_n^0, omega_n^1, .., omega_n^(n-1).
        out[k] = 1/2 * (even_out[k] + omega * odd_out[k])
        out[k + n//2] = 1/2 * (even_out[k] - omega * odd_out[k])
        omega *= principal_root_of_unity
    
    if not has_imaginary:
        # This will return a cleaner inverse by discarding imag parts whose 
        # absolute value is less than imag_threshold
        out = [item.real if abs(item.imag) < imag_threshold else item for item in out]
    return out

def fft_iterative(poly: Sequence) -> List:
    """Perform iterative discrete fast Fourier transform (DFT) of a polynomial with a degree that is `2^t-1`, t being a positive integer (ie `len(poly)` should be an exact power of 2).
    
    Input is coeffcient form, output is point-value form (values are complex numbers).
    """
    # For algo detail, cf. CLRS Ch30.3.
    # Time complexity: Theta(N log N), but the const in Theta is smaller than that in 
    # fft_recursive()
    
    n = len(poly)
    if n == 1:
        return poly
    
    bit_reversed_poly = _bit_reversal_permutation(poly)
    for s in range(1, int(math.log2(n) + 1)):
        # s is the level of recursion counting from bottom, lowest being 1, 2nd-highest 
        # (ie the level just below the root = the orig list) being log2(n).
        
        # Length of the target sublists in level s+1 (eg for s=1, target is len of lv2)
        target_len = 2 ** s
        # Compute omega_{target_len}
        principal_root_of_unity = cmath.exp((2 * cmath.pi / target_len) * 1j)
        for k in range(0, n, target_len):
            omega = 1
            for j in range(target_len // 2):
                body = bit_reversed_poly[k + j]
                twiddle = omega * bit_reversed_poly[k + j + target_len // 2]
                # Butterfly operation in-place
                bit_reversed_poly[k + j] = body + twiddle
                bit_reversed_poly[k + j + target_len // 2] = body - twiddle
                omega *= principal_root_of_unity
    
    return bit_reversed_poly

def inverse_fft_iterative(
    poly: Sequence, has_imaginary: bool = False, imag_threshold: float = 1e-14
) -> List:
    """Perform inverse iterative discrete fast Fourier transform (DFT) of a polynomial with a degree that is `2^t-1`, t being a positive integer (ie `len(poly)` should be an exact power of 2).
    
    Input is point-value form, output is coefficient form.
    """
    # For algo detail, cf. CLRS Ch30.3.
    # Time complexity: Theta(N log N), but the const in Theta is smaller than that in 
    # fft_recursive()
    
    n = len(poly)
    if n == 1:
        return poly
    
    bit_reversed_poly = _bit_reversal_permutation(poly)
    for s in range(1, int(math.log2(n) + 1)):
        # s is the level of recursion counting from bottom, lowest being 1, 2nd-highest 
        # (ie the level just below the root = the orig list) being log2(n).
        
        # Length of the target sublists in level s+1 (eg for s=1, target is len of lv2)
        target_len = 2 ** s
        # Compute omega_{target_len}
        principal_root_of_unity = cmath.exp(-(2 * cmath.pi / target_len) * 1j)
        for k in range(0, n, target_len):
            omega = 1
            for j in range(target_len // 2):
                body = bit_reversed_poly[k + j]
                twiddle = omega * bit_reversed_poly[k + j + target_len // 2]
                # Butterfly operation in-place
                bit_reversed_poly[k + j] = 1/2 * (body + twiddle)
                bit_reversed_poly[k + j + target_len // 2] = 1/2 * (body - twiddle)
                omega *= principal_root_of_unity
    
    if not has_imaginary:
        # This will return a cleaner inverse by discarding imag parts whose 
        # absolute value is less than imag_threshold
        bit_reversed_poly = [item.real if abs(item.imag) < imag_threshold else item for item in bit_reversed_poly]
    return bit_reversed_poly

def _bit_reversal_permutation(poly: Sequence) -> List:
    # Perform bit-reversal permutation, eg. [01234567] -> [04261537].
    # In binary form, the desired sequence is 000 100 010 110 001 101 011 111, 
    # and when we reverse the bits of each:   000 001 010 011 100 101 110 111 (ie orig).
    # Time complexity: Theta(N log N)
    bit_reversed_poly = [None] * len(poly)
    for k in range(len(poly)):
        # Compute the log(len)-bit integer formed by reversing the bits of binary-form k
        # Note: We need to convert the reversed binary-form int to decimal-form.
        # In the f-string below, `08b` means pad with 0, fieldwidth 8, b for binary.
        # [::-1] reverses a list.
        width = int(math.log2(len(poly)))
        reverse_bit = int(f"{k:0{width}b}"[::-1], base=2)
        bit_reversed_poly[reverse_bit] = poly[k]
    return bit_reversed_poly


##########################################
### Test client

# Multiply: brute force

jovian.evaluate_test_cases(func=poly_multiply_basic, test_cases=tests)

# Multiply: FFT iterative
# Note: The next line uses the default value `iterative` for kwarg `method`
jovian.evaluate_test_cases(func=poly_multiply_fft, test_cases=tests)

# Multiply: FFT recursive
jovian.evaluate_test_cases(
    func=poly_multiply_fft, test_cases=tests, extra_func_kwargs={'method': 'recursive'}
)

jovian.evaluate_test_cases_justyre(
    func=poly_multiply_fft, tests=tests, extra_func_kwargs={'method': 'recursive'}
)