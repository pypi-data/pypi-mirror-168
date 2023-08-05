"""This module implements the SafeResult data structure."""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class SafeResult:
    """A data structure used to capture the result of a function call."""

    value: Optional[Any] = None
    error: Optional[Exception] = None

    @property
    def has_error(self) -> bool:
        """Returns True if the result has an error."""
        return self.error is not None
