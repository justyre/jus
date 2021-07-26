# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Tree exception definitions."""

from typing import Any


class DuplicateKeyError(Exception):
    """Raised when a key already exists. Inherited from `Exception` class."""
    
    def __init__(self, key: Any) -> None:
        Exception.__init__(self, f"A node with key {str(key)} already exists.")