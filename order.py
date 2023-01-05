from abc import ABC, abstractmethod
from quiver import _Path


class PathOrder(ABC):
    @abstractmethod
    def _isLessThan(self, path1: _Path, path2: _Path) -> bool:
        pass


class DegLex(PathOrder):
    """Degree lexicographical order on paths. First compares the
    length of a path (number of arrows), longest paths is largest.
    For paths of equal length, compares arrows lexicographically
    for the usual order on integers."""

    def _isLessThan(self, path1: _Path, path2: _Path) -> bool:
        if len(path1) == len(path2):
            return path1.monomial < path2.monomial
            # Lexicographical order of lists already implemented in Python.
        else:
            return len(path1) < len(path2)
