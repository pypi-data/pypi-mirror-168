import importlib.metadata


try:
    __version__ = importlib.metadata.version(__package__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.1.0"

__all__ = ["SafeResult", "safely"]

from .api import safely
from .core import SafeResult
