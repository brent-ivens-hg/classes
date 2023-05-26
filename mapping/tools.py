"""
Dicttools
"""
from typing import TypeVar
from collections.abc import Mapping
# LOCAL #

_KT = TypeVar('_KT')
_VT = TypeVar('_VT')


def invert_keep_first(mapping: Mapping[_KT, _VT]) -> dict[_VT, _KT]:
    """
    >>> invert_keep_first({0: 'A', 1: 'B', 2: 'B'})
    {'A': 0, 'B': 1}
    """
    res = {}
    for key, value in mapping.items():
        res.setdefault(value, key)
    return res


def invert_keep_last(mapping: Mapping[_KT, _VT]) -> dict[_VT, _KT]:
    """
    >>> invert_keep_last({0: 'A', 1: 'B', 2: 'B'})
    {'A': 0, 'B': 2}
    """
    return {value: key for key, value in mapping.items()}


def invert_keep_all(mapping: Mapping[_KT, _VT]) -> dict[_VT, list[_KT]]:
    """
    >>> invert_keep_all({0: 'A', 1: 'B', 2: 'B'})
    {'A': [0], 'B': [1, 2]}
    """
    res = {}
    for key, value in mapping.items():
        res.setdefault(value, []).append(key)
    return res


if __name__ == '__main__':
    import doctest

    doctest.testmod()
