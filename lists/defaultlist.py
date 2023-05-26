"""
List stuff
"""
from __future__ import annotations

from collections.abc import Iterable
from typing import TypeVar
# LOCAL #
from utils.missing import MISSING

_T = TypeVar('_T')
_VT = TypeVar('_VT')


# noinspection PyPep8Naming
class defaultlist(list):
    def __init__(self, iterable: Iterable[_T] = MISSING, default: _VT = None) -> None:
        if iterable is MISSING:
            iterable = []
        self.default = default
        super().__init__(iterable)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.default}, {self})'

    def __str__(self) -> str:
        return super().__repr__()

    def __add__(self, other) -> defaultlist:
        return defaultlist(super().__add__(other))

    def __mul__(self, other) -> defaultlist:
        return defaultlist(super().__mul__(other))

    __rmul__ = __mul__

    def __getitem__(self, item: int or slice) -> _T | _VT:
        try:
            result = super().__getitem__(item)
            if type(result) is not list:
                return result
            return defaultlist(result, self.default)
        except IndexError:
            return self.default

    def index(self, value: _T, start: int = ..., stop: int = ...) -> int:
        try:
            return super().index(slice(value, start, stop))
        except ValueError:
            return self.default


def doctest_defaultlist() -> None:
    """
    list with default value
    >>> lst = defaultlist(list(range(10)), -1)
    >>> lst
    defaultlist(-1, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> lst = defaultlist(list(range(10)), -1)
    >>> str(lst)
    '[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]'
    >>> lst = defaultlist(list(range(10)), -1)
    >>> lst[3]
    3
    >>> lst[80]
    -1
    >>> lst[9]
    9
    >>> lst[-1]
    9
    >>> list()[0]
    Traceback (most recent call last):
    IndexError: list index out of range
    >>> defaultlist()[0]
    >>> list().index('1')
    Traceback (most recent call last):
    ValueError: '1' is not in list
    >>> defaultlist().index('1')

    >>> l = defaultlist((1, 2, 3))
    >>> l.append(4)
    >>> l[0] = -1
    >>> l[:2] = defaultlist((10, 11))
    >>> isinstance(l, defaultlist)
    True
    >>> l3 = l + defaultlist((4, 5, 6))
    >>> isinstance(l3, defaultlist)
    True
    >>> l4 = 3 * l
    >>> isinstance(l4, defaultlist)
    True
    >>> l5 = l[:2]
    >>> isinstance(l5, defaultlist)
    True
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
