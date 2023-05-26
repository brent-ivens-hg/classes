"""
Ranged Class
"""
from __future__ import annotations

from typing import Any, Type
# LOCAL #
from utils.missing import MISSING

__all__ = ['Ranged', 'RangedException']


# noinspection SpellCheckingInspection
Rangedable = dict | list | set | tuple


class RangedException(Exception):
    pass


class Ranged:
    def __init__(self, factory: Type[Rangedable], default: Any = MISSING) -> None:
        if factory not in {dict, list, set, tuple}:
            raise RangedException(f'{factory} is not a valid factory type')

        self.factory = factory

        if factory is dict:
            self.default = None if default is MISSING else default
        elif default is not MISSING:
            raise RangedException(f'{factory} does not support default parameter')

    def __repr__(self) -> str:
        if self.factory is not dict:
            return f'{self.__class__.__name__}({self.factory})'
        return f'{self.__class__.__name__}({self.factory}, default={self.default})'

    def __eq__(self, other: Ranged) -> bool:
        if type(other) is not Ranged:
            return False
        if self.factory is not other.factory:
            return False
        if self.factory is dict:
            return self.default == other.default
        return True

    def __getitem__(self, item: int | slice) -> Rangedable:
        if isinstance(item, int):
            item = slice(item)
        elif not isinstance(item, slice):
            raise RangedException('invalid syntax')
        if item.start == item.stop == item.step is None: return self.factory()  # empty
        if item.stop is None or item.step == 0: raise RangedException('invalid syntax')  # infinite
        R = range(item.start or 0, item.stop, item.step or 1)
        if hasattr(self, 'default'): return dict.fromkeys(R, self.default)
        return self.factory(R)


def doctest_ranged() -> None:
    """
    # INITIALIZATION #
    >>> Ranged(dict)
    Ranged(<class 'dict'>, default=None)
    >>> Ranged(list)
    Ranged(<class 'list'>)
    >>> Ranged(set)
    Ranged(<class 'set'>)
    >>> Ranged(tuple)
    Ranged(<class 'tuple'>)
    >>> Ranged(int)
    Traceback (most recent call last):
    RangedException: <class 'int'> is not a valid factory type

    # INITIALIZATION WITH DEFAULT PARAMETER #
    >>> Ranged(dict, 1)
    Ranged(<class 'dict'>, default=1)
    >>> Ranged(list, 1)
    Traceback (most recent call last):
    RangedException: <class 'list'> does not support default parameter
    >>> Ranged(set, 1)
    Traceback (most recent call last):
    RangedException: <class 'set'> does not support default parameter
    >>> Ranged(tuple, 1)
    Traceback (most recent call last):
    RangedException: <class 'tuple'> does not support default parameter

    # EQUALS #
    >>> Ranged(dict) == {}
    False
    >>> Ranged(list) == []
    False
    >>> Ranged(set) == {...}
    False
    >>> Ranged(tuple) == ()
    False
    >>> Ranged(dict) == Ranged(dict, None)
    True
    >>> Ranged(dict) == Ranged(dict, False)
    False
    >>> Ranged(dict) == Ranged(dict, 0)
    False
    >>> Ranged(dict, 0) == Ranged(dict, 0)
    True
    >>> Ranged(dict, 0) == Ranged(dict, False)
    True
    >>> Ranged(dict) == Ranged(dict)
    True
    >>> Ranged(list) == Ranged(list)
    True
    >>> Ranged(set) == Ranged(set)
    True
    >>> Ranged(tuple) == Ranged(tuple)
    True
    >>> Ranged(dict) == Ranged(list)
    False
    >>> Ranged(dict) == Ranged(set)
    False
    >>> Ranged(dict) == Ranged(tuple)
    False
    >>> Ranged(list) == Ranged(set)
    False
    >>> Ranged(list) == Ranged(tuple)
    False
    >>> Ranged(set) == Ranged(tuple)
    False

    # INDEXING #
    >>> Ranged(list)[:]
    []
    >>> Ranged(list)[::]
    []
    >>> Ranged(list)[None:None:None]
    []
    >>> Ranged(list)[0]
    []
    >>> Ranged(list)[-1]
    []
    >>> Ranged(list)[10]
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> Ranged(list)[False]
    []
    >>> Ranged(list)[True]
    [0]
    >>> Ranged(list)[2:10:]
    [2, 3, 4, 5, 6, 7, 8, 9]
    >>> Ranged(list)[:10:2]
    [0, 2, 4, 6, 8]
    >>> Ranged(list)[0::0] # RangedException
    Traceback (most recent call last):
    RangedException: invalid syntax
    >>> Ranged(list)[None::None]
    []
    >>> Ranged(list)[2:10:2]
    [2, 4, 6, 8]
    >>> Ranged(list)[10:-1:-1]
    [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    >>> Ranged(dict)[5]  # implicit
    {0: None, 1: None, 2: None, 3: None, 4: None}
    >>> Ranged(dict, None)[5]  # explicit
    {0: None, 1: None, 2: None, 3: None, 4: None}
    >>> Ranged(dict, 69)[5]
    {0: 69, 1: 69, 2: 69, 3: 69, 4: 69}
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
