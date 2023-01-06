from __future__ import annotations
from abc import ABC, abstractmethod
from functools import total_ordering
from itertools import product
import printing


class PathOrder(ABC):
    @abstractmethod
    def _isLessThan(self, path1: _Path, path2: _Path) -> bool:
        pass


class DegLex(PathOrder):
    def _isLessThan(self, path1: _Path, path2: _Path) -> bool:
        if len(path1) == len(path2):
            return path1.monomial < path2.monomial
        else:
            return len(path1) < len(path2)


class PathFactory:
    def __init__(self, order: PathOrder) -> None:
        self.order = order

    def createPath(
        self,
        source: int,
        monomial: list[int],
        target: int,
        quiver: Quiver,
    ):
        return _Path(source, monomial, target, quiver, self.order)


@total_ordering
class _Path:
    def __init__(
        self,
        source: int,
        vars: list[int],
        target: int,
        quiver: Quiver,
        order: PathOrder = DegLex(),
        isEmpty: bool = False,
    ) -> None:

        if vars:
            assert source == quiver.source[vars[0]], ValueError(
                f"""Vertex {source} is not the source {quiver.source[vars[0]]} of arrow {vars[0]}."""
            )
            assert target == quiver.target[vars[-1]], ValueError(
                f"Vertex {target} is not the target {quiver.target[vars[-1]]} of arrow {vars[-1]}."
            )
            _assertArrowsInQuiver(vars, quiver)

        self.source = source
        self.target = target
        self.quiver = quiver
        self.monomial = vars
        self.order = order
        self.nonePath = isEmpty

    def __len__(self) -> int:
        return len(self.monomial)

    def __str__(self) -> str:
        result = ""

        if not self.monomial:
            return "e" + printing.toSub(self.source)

        last = self.monomial[0]
        exponent = 1
        for number in self.monomial[1:]:
            if last == number:
                exponent += 1
                last = number
                continue
            else:
                var = printing.toVar(last)
                result += var + printing.toSup(exponent)
                last = number
                exponent = 1

        return result + printing.toVar(last) + printing.toSup(exponent)

    def __add__(self, other: _Path) -> _Path:
        """Computes the concatenation of two paths or
        returns None if the paths are not composable."""

        assert self.quiver == other.quiver, ValueError(
            "Cannot concatenate paths from different quivers."
        )
        if self.target == other.source:
            return _Path(
                self.source,
                self.monomial + other.monomial,
                other.target,
                self.quiver,
            )
        else:
            return _nonePath(self.quiver, self.order)

    def __invert__(self) -> _Path:
        """Returns the opposite of a path, which in particular
        is a path in the opposite quiver, by reversing all arrows
        and source and target."""

        quiver = ~(self.quiver)
        monomial = self.monomial[::-1]
        return _Path(self.target, monomial, self.source, quiver)

    def __eq__(self, other: _Path) -> bool:
        return all(
            [
                self.source == other.source,
                self.target == other.target,
                self.monomial == other.monomial,
                self.quiver == other.quiver,
                # self.order == other.order,
            ]
        )

    def __hash__(self):
        return hash(
            (
                self.source,
                self.monomial,
                self.target,
                self.quiver,
                self.order,
            )
        )

    def __lt__(self, other: _Path) -> bool:
        return self.order._isLessThan(self, other)

    def _find(self, other: _Path) -> int:
        """Check if the path is divisible by another path. If it is,
        return the first index where it appears as a subpath. If
        there is no such index, return -1."""
        # NOTE: Expected to be used with paths of small length (say
        # at most 100) so the naive linear search is more that enough.

        if len(self) < len(other):
            return -1
        else:
            for i in range(len(self) - len(other) + 1):
                divisor = self.monomial[i : i + len(other)]
                if divisor == other.monomial:
                    return i
        return -1

    def _replaceBy(
        self,
        new_path: _Path,
        position_found: int,
        old_path_length: int,
    ) -> _Path:
        """Replace the subpath of self starting at position i
        and ending at position j with the other path."""
        assert position_found > -1

        new_monomial = (
            self.monomial[:position_found]
            + new_path.monomial
            + self.monomial[position_found + old_path_length :]
        )
        return _Path(
            self.quiver.source[new_monomial[0]],
            new_monomial,
            self.quiver.target[new_monomial[-1]],
            self.quiver,
            self.order,
        )


def _nonePath(quiver: Quiver, order: PathOrder) -> _Path:
    return _Path(0, [], 0, quiver, order, isEmpty=True)


class Quiver:
    def __init__(
        self,
        q0: list[int],
        q1: list[int],
        s: dict[int, int],
        t: dict[int, int],
        name: str = "QQ",
    ) -> None:
        assert q0, ValueError("Cannot initialize quiver with no vertices.")
        assert set(s.keys()) == set(q1), ValueError(
            "Source function must have domain equal to arrows."
        )
        assert set(t.keys()) == set(q1), ValueError(
            "Target function must have domain equal to arrows."
        )
        assert set(s.values()).issubset(set(q0)), ValueError(
            "Source function must have image contained in vertices."
        )
        assert set(t.values()).issubset(set(q0)), ValueError(
            "Target function must have image contained in vertices."
        )

        self.nodes = q0
        self.arrows = q1
        self.source = s
        self.target = t
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __invert__(self) -> Quiver:
        """Return the opposite of the quiver by interchanging the
        source and target functions."""
        return Quiver(
            self.nodes,
            self.arrows,
            self.target,  # Target and source interchanged.
            self.source,
            name=f"{self.name}-OP",
        )

    def __eq__(self, other: Quiver) -> bool:
        """Check if two quivers are equal, by verifying that the
        arrow and node sets are equal, and that the source and
        target functions are equal.

        WARNING: Isomorphic quivers can be different."""
        return all(
            [
                self.arrows == other.arrows,
                self.nodes == other.nodes,
                self.target == other.target,
                self.source == other.source,
            ]
        )

    def _incomingArrows(self, v: int) -> list[_Path]:
        """Return the list of arrows in the quiver that are incoming at vertex v
        as Path objects."""
        assert v in set(self.nodes), ValueError("Input vertex must be in the quiver.")

        return [
            _Path(
                self.source[arrow],
                [arrow],
                self.target[arrow],
                self,
            )
            for arrow in [u for u in set(self.target.keys()) if self.target[u] == v]
        ]

    def _outgoingArrows(self, v: int) -> list[_Path]:
        """Return the list of arrows in the quiver that are outgoing at vertex
        v as Path objects."""
        assert v in set(self.nodes), ValueError("Input vertex must be in the quiver.")
        return [~path for path in (~self)._incomingArrows(v)]

    def _extendPathByIncomingArrows(self, path: _Path) -> list[_Path]:
        """Given a path encoded as a list of integers, find all paths of the form
        arrow * path in the quiver where arrow is incoming at path."""
        paths = [arrow + path for arrow in self._incomingArrows(path.source)]
        return [path for path in paths if path]

    def _extendPathByOutgoingArrows(self, path: _Path) -> list[_Path]:
        """Given a path encoded as a list of integers find all paths of the form
        path * arrow in the quiver where arrow is outgoing at path."""
        return [~path for path in (~self)._extendPathByIncomingArrows(~path)]

    def allPathsOutOf(self, v: int, length: int) -> list[_Path]:
        """Return the set of all paths in the quiver whose source is vertex v."""
        result = []
        assert length > -1, ValueError("Length must be non-negative.")

        if length == 0:
            return [_Path(v, [], v, self)]

        if length == 1:
            return self._outgoingArrows(v)
        else:
            new_paths = self.allPathsOutOf(v, 1)
            result = new_paths[::]
            counter = 1
            while counter < length:
                old_paths = new_paths[::]
                new_paths = []
                """Append all possible outgoing vertices"""
                for path in old_paths:
                    new = self._extendPathByOutgoingArrows(path)
                    new_paths.extend(new)
                    result.extend(new)
                counter += 1
        return result

    def allPathsInto(self, v: int, length: int) -> list[_Path]:
        """Return the set of all paths in the quiver whose target is v.
        The stationary path at v is always ignored."""
        return [~path for path in (~self).allPathsOutOf(v, length)]

    def pathsFromTo(self, v: int, w: int, length: int) -> list[_Path]:
        """Return the set of all paths from v to w up to the given length."""
        assert length > -1, ValueError("Length must be non-negative.")

        if length == 0:
            if v != w:
                return []
            else:
                return [_Path(v, [], v, self)]

        if length == 1:
            # TODO: Can optimize by picking v or w depending on size of out(v) or in(w).
            # Can use {}^OP to easily change between v and w.
            return [path for path in self._incomingArrows(w) if path.source == v]

        else:
            part1 = self.allPathsOutOf(v, 1)
            part2 = self.allPathsInto(w, length - 1)
            # TODO: optimize the size of |part1||part2|?
            paths = [
                a1 + a2 for a1, a2 in product(part1, part2) if a1.target == a2.source
            ]
            # The last IF already makes sure that no path in paths is None.
            return [path for path in paths if path]

    def arrowIdeal(self, length: int, top=False) -> list[_Path]:
        """Return a list of all Paths  in Q up to the specified length.
        Paths are listed according to the degree lexicographical order.
        If top is set to True, prints only the paths of maximal length
        that are obtained."""

        result = []
        for a, b in product(self.nodes, self.nodes):
            result.extend(self.pathsFromTo(a, b, length))
        result.sort()

        if top:
            return [path for path in result if len(path) == length]
        else:
            return result


def _assertArrowsInQuiver(monomial: list[int], quiver: Quiver) -> None:
    """Helper function to verify that a path initialized to live in a
    given quiver has its arrows in that quiver and these arrows are
    composable."""
    for i in range(len(monomial)):
        assert monomial[i] in quiver.arrows, ValueError(
            f"Arrow {monomial[i]} at position {i} does not belong to quiver {quiver}."
        )
        if i < len(monomial) - 1:
            assert (
                quiver.target[monomial[i]] == quiver.source[monomial[i + 1]]
            ), ValueError(
                f"""
    * Non-concatenble arrows at position {i}.
    * Issue: ───{monomial[i]}───> {quiver.target[monomial[i]]} (!) {quiver.source[monomial[i + 1]]} ───{monomial[i+1]}───>"""
            )
