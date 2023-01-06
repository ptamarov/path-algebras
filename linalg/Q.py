from __future__ import annotations
from .field import Field, FieldScalar
from typing import Tuple


class Rational(FieldScalar):
    def __init__(self, numerator: int, denominator: int = 1) -> None:
        d = gcd(numerator, denominator)

        if denominator < 0:
            numerator = -numerator
            denominator = -denominator

        self.numerator = numerator // d
        self.denominator = denominator // d

    def __lt__(self, other) -> bool:
        assert isinstance(other, Rational)
        return self.numerator * other.denominator < self.denominator * other.numerator

    def __dict__(self) -> dict:
        return {"numerator": self.numerator, "denomintaor": self.denominator}

    def __eq__(self, other) -> bool:
        assert isinstance(other, Rational)
        return (self.numerator == other.numerator) and (
            self.denominator == other.denominator
        )

    def __str__(self) -> str:
        return f"{self.numerator}" + ("╱" + str(self.denominator)) * (
            self.denominator != 1
        )

    def __add__(self, other) -> Rational:
        assert isinstance(other, Rational)
        return Rational(
            self.numerator * other.denominator + self.denominator * other.numerator,
            self.denominator * other.denominator,
        )

    def __mul__(self, other) -> Rational:
        return other.__rmul__(self)

    def __rmul__(self, other) -> Rational:
        return Rational(
            self.numerator * other.numerator, self.denominator * other.denominator
        )

    def __neg__(self) -> Rational:
        return Rational(-self.numerator, self.denominator)

    def __sub__(self, other) -> Rational:
        assert isinstance(other, Rational)
        return self + (-other)

    def __invert__(self) -> Rational:
        """Return the inverse of an element."""
        assert self != self._getFieldZero(), "Cannot invert the zero element."
        return Rational(self.denominator, self.numerator)

    def __truediv__(self, other) -> Rational:
        assert other != self._getFieldZero(), "Cannot divide by zero."
        return self * ~other

    def _getFieldZero(self) -> Rational:
        return Rational(0)

    def _getFieldOne(self) -> Rational:
        return Rational(1)

    def evaluate(self, digits=10):
        return round(self.numerator / self.denominator, digits)

    def floor(self) -> int:
        """Returns the floor of a rational number as an integer."""
        return self.numerator // self.denominator

    def fractional(self) -> Rational:
        """Returns the fractional part of the rational number."""
        return self - self.floor()

    def intfrac(self) -> Tuple[int, Rational]:
        """Returns the tuple n: int, r: Rational where n is the floor
        of the rational number and r is its fractonal part."""
        return self.floor(), self.fractional()

    def continued(self, stopper=None) -> list[int]:
        """Returns the continued fraction representation of a given
        rational number.
        """

        current: Rational = self
        f: int = current.floor()
        diff: Rational = current - Rational(f)
        result = [f]

        while diff != Rational(0):
            current = ~diff
            f = current.floor()
            diff = current - Rational(current.floor())
            result.append(f)
        return result


class QQ(Field):
    def __init__(self, char=0):
        self.char = char
        self.scalars = Rational

    def getOne(self) -> FieldScalar:
        return Rational(1)

    def getZero(self) -> FieldScalar:
        return Rational(0)


def regular_continued(array) -> Rational:
    if len(array) == 0:
        return Rational(1)

    else:
        return array[0] + Rational(1) / regular_continued(array[1:])


def sqrt(n: int, approx: int = 10) -> Rational:
    assert n >= 0, ValueError("Input must be a non-negative integer.")
    a = 0
    while n > a**2:
        a += 1

    d = n - (a - 1) ** 2
    result = Rational(a)

    counter = 0

    if d == 0:
        return result

    while counter < approx:
        result = Rational(a) + Rational(d) / (Rational(a) + result)
        counter += 1

    return result


def gcd(m: int, n: int) -> int:
    while abs(n) > 0:
        m, n = n, m % n
    return abs(m)
