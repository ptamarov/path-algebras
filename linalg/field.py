from __future__ import annotations
from abc import ABC, abstractmethod


class FieldScalar(ABC):
    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __add__(self, other) -> FieldScalar:
        pass

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    @abstractmethod
    def __mul__(self, other) -> FieldScalar:
        pass

    @abstractmethod
    def __sub__(self, other) -> FieldScalar:
        pass

    @abstractmethod
    def __neg__(self) -> FieldScalar:
        pass

    @abstractmethod
    def __invert__(self) -> FieldScalar:
        assert self != self._getFieldZero(), "Cannot invert the zero element."
        pass

    @abstractmethod
    def __truediv__(self, other) -> FieldScalar:
        assert other != self._getFieldZero(), "Cannot divide by zero."
        pass

    @staticmethod
    @abstractmethod
    def _getFieldZero() -> FieldScalar:
        pass

    @staticmethod
    @abstractmethod
    def _getFieldOne() -> FieldScalar:
        pass


class Field(ABC):
    def __init__(self, char=0) -> None:
        self.char = char
        self.scalars = FieldScalar

    @abstractmethod
    def getZero(self) -> FieldScalar:
        pass

    @abstractmethod
    def getOne(self) -> FieldScalar:
        pass
