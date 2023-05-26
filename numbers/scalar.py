from __future__ import annotations

import operator as op

from collections import abc
from dataclasses import dataclass
from itertools import repeat
from typing import Generic, TypeVar

__all__ = ['Scalar']

_T = TypeVar('_T')
_S = TypeVar('_S')


@dataclass(frozen=True, slots=True, order=True)
class Scalar(Generic[_T]):
    """
    Scalar Object
    """

    value: _T

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.value!r})'

    # BINARY OPERATIONS

    def _binop(self, other: T_Scalable, func: abc.Callable[[_T, T_Scalable], _S]) -> S_Scalable:
        if isinstance(other, Scalar):
            return Scalar(func(self.value, other.value))
        try:
            return map(func, repeat(self.value), other)
        except TypeError:
            return Scalar(func(self.value, other))

    def _rbinop(self, other: T_Scalable, func: abc.Callable[[T_Scalable, _T], _S]) -> S_Scalable:
        if isinstance(other, Scalar):
            return func(other.value, self.value)
        try:
            return map(func, other, repeat(self.value))
        except TypeError:
            return func(other, self.value)

    def __add__(self, other: T_Scalable) -> map:
        return self._binop(other, op.add)

    def __radd__(self, other: T_Scalable) -> map:
        return self._rbinop(other, op.add)

    def __sub__(self, other: T_Scalable) -> map:
        return self._binop(other, op.sub)

    def __rsub__(self, other: T_Scalable) -> map:
        return self._rbinop(other, op.sub)

    def __mul__(self, other: T_Scalable) -> map:
        return self._binop(other, op.mul)

    def __rmul__(self, other: T_Scalable) -> map:
        return self._rbinop(other, op.mul)

    def __truediv__(self, other: T_Scalable) -> map:
        return self._binop(other, op.truediv)

    def __rtruediv__(self, other: T_Scalable) -> map:
        return self._rbinop(other, op.truediv)

    def __floordiv__(self, other: T_Scalable) -> map:
        return self._binop(other, op.floordiv)

    def __rfloordiv__(self, other: T_Scalable) -> map:
        return self._rbinop(other, op.floordiv)

    def __pow__(self, other: T_Scalable) -> map:
        return self._binop(other, op.pow)

    def __rpow__(self, other: T_Scalable) -> map:
        return self._rbinop(other, op.pow)

    def __mod__(self, other: T_Scalable) -> map:
        return self._binop(other, op.mod)

    def __rmod__(self, other: T_Scalable) -> map:
        return self._rbinop(other, op.mod)

    # BITWISE OPERATORS

    def __lshift__(self, other: T_Scalable) -> map:
        return self._binop(other, op.lshift)

    def __rlshift__(self, other: T_Scalable) -> map:
        return self._rbinop(other, op.lshift)

    def __rshift__(self, other: T_Scalable) -> map:
        return self._binop(other, op.rshift)

    def __rrshift__(self, other: T_Scalable) -> map:
        return self._rbinop(other, op.rshift)

    def __and__(self, other: T_Scalable) -> map:
        return self._binop(other, op.and_)

    def __rand__(self, other: T_Scalable) -> map:
        return self._rbinop(other, op.and_)

    def __or__(self, other: T_Scalable) -> map:
        return self._binop(other, op.or_)

    def __ror__(self, other: T_Scalable) -> map:
        return self._rbinop(other, op.or_)

    def __invert__(self):
        return op.invert(self.value)

    def __xor__(self, other: T_Scalable) -> map:
        return self._binop(other, op.xor)

    def __rxor__(self, other: T_Scalable) -> map:
        return self._rbinop(other, op.xor)


T_Scalable = _T | Scalar[_T] | abc.Iterable[_T]
S_Scalable = _S | Scalar[_S] | abc.Iterable[_S]


def doctest_numeric_scalar():
    """
    >>> k = Scalar(2)

    >>> 2 + k

    >>> list(k + [1, 2, 3]), list([1, 2, 3] + k)              # Numeric Addition
    ([3, 4, 5], [3, 4, 5])
    >>> list(k - [1, 2, 3]), list([1, 2, 3] - k)              # Numeric Subtraction
    ([1, 0, -1], [-1, 0, 1])
    >>> list(k * [1, 2, 3]), list([1, 2, 3] * k)              # Numeric Multiplication
    ([2, 4, 6], [2, 4, 6])
    >>> list(k / [1, 2, 3]), list([1, 2, 3] / k)              # Numeric Division
    ([2.0, 1.0, 0.6666666666666666], [0.5, 1.0, 1.5])
    >>> list(k // [1, 2, 3]), list([1, 2, 3] // k)            # Numeric Floor Division
    ([2, 1, 0], [0, 1, 1])
    >>> list(k ** [1, 2, 3]), list([1, 2, 3] ** k)            # Numeric Power
    ([2, 4, 8], [1, 4, 9])
    >>> list(k % [1, 2, 3]), list([1, 2, 3] % k)              # Numeric Modulo
    ([0, 0, 2], [1, 0, 1])
    >>> list(k & [1, 2, 3]), list([1, 2, 3] & k)              # Numeric And
    ([0, 2, 2], [0, 2, 2])
    >>> list(k | [1, 2, 3]), list([1, 2, 3] | k)              # Numeric Or
    ([3, 2, 3], [3, 2, 3])
    >>> list(k ^ [1, 2, 3]), list([1, 2, 3] ^ k)              # Numeric Xor
    ([3, 0, 1], [3, 0, 1])
    >>> list(k << [1, 2, 3]), list([1, 2, 3] << k)            # Numeric Left Shift
    ([4, 8, 16], [4, 8, 12])
    >>> list(k >> [1, 2, 3]), list([1, 2, 3] >> k)            # Numeric Right Shift
    ([1, 0, 0], [0, 0, 0])
    >>> list(k * ['a', 'b', 'c']), list(['a', 'b', 'c'] * k)  # Numeric Object Multiplication
    (['aa', 'bb', 'cc'], ['aa', 'bb', 'cc'])
    >>> list(k * [[1], [2], [3]]), list([[1], [2], [3]] * k)
    ([[1, 1], [2, 2], [3, 3]], [[1, 1], [2, 2], [3, 3]])
    """


def doctest_non_numeric_scalar():
    """
    >>> k = Scalar('a')
    >>> # String Addition
    >>> list(k + ['a', 'b', 'c']), list(['a', 'b', 'c'] + k)
    (['aa', 'ab', 'ac'], ['aa', 'ba', 'ca'])
    >>> # String Modulo
    >>> list(['%s', '%s', '%s'] % k)
    ['a', 'a', 'a']
    >>> k = Scalar([1])
    >>> # List Addition
    >>> list(k + [[1], [2], [3]]), list([[1], [2], [3]] + k)
    ([[1, 1], [1, 2], [1, 3]], [[1, 1], [2, 1], [3, 1]])
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
