from __future__ import annotations
from .field import Field, FieldScalar


class Vector:
    def __init__(self, field: Field, *args: FieldScalar):
        assert len(args) > 0, ValueError("Cannot initialize empty vector.")
        self.array = args
        self.field = field

    def __str__(self) -> str:
        out = "("
        for entry in self.array[:-1]:
            out += str(entry) + ", "
        out += str(self.array[-1])
        out += ")"

        return out

    def __len__(self) -> int:
        return len(self.array)

    def __add__(self, other) -> Vector:
        assert isinstance(other, Vector), TypeError(
            f"Cannot add {type(self)} to {type(other)}."
        )
        assert len(self) == len(other), ValueError(
            f"Lengths {len(self)} and {len(other)} are incompatible."
        )
        array = [a + b for a, b in zip(self.array, other.array)]
        return Vector(self.field, *array)

    def __neg__(self) -> Vector:
        return Vector(self.field, *[-scalar for scalar in self.array])

    def __sub__(self, other) -> Vector:
        return self + (-other)

    def __rmul__(self, other: FieldScalar) -> Vector:
        return Vector(self.field, *[scalar * other for scalar in self.array])

    def __mul__(self, other: FieldScalar) -> Vector:
        return Vector(self.field, *[scalar * other for scalar in self.array])

    def dotProduct(self, other: Vector) -> FieldScalar:
        assert len(self) == len(other), ValueError(
            f"Lengths {len(self)} and {len(other)} are incompatible."
        )

        result = self.field.getZero()
        for a, b in zip(self.array, other.array):
            result += a * b
        return result


def zeroVector(field: Field, n: int) -> Vector:
    assert n > 0, ValueError("Cannot create a vector of non-positive length.")
    zero = field.getZero()
    return Vector(field, *[zero for _ in range(n)])
