"""
Unordered Pair
"""
from typing import Generic, TypeVar

_T1 = TypeVar('_T1')
_T2 = TypeVar('_T2')


class UnorderedPair(Generic[_T1, _T2]):
    def __init__(self, __1: _T1, __2: _T2, /) -> None:
        self.__1 = __1
        self.__2 = __2

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}{self.__1, self.__2}'

    def __len__(self) -> int:
        return 2

    def __getitem__(self, index: int) -> _T1 | _T2:
        if index == 0: return self.__1
        if index == 1: return self.__2
        raise IndexError('pair index out of range')

    def __invert__(self) -> 'UnorderedPair[_T2, _T1]':
        return self.__class__(self.__2, self.__1)

    def __eq__(self, other: 'UnorderedPair') -> bool:
        if not isinstance(other, UnorderedPair): return False
        return (self.__1 == other.__1 and self.__2 == other.__2
                or
                self.__1 == other.__2 and self.__2 == other.__1)

    def __hash__(self) -> int:
        return hash((UnorderedPair, frozenset({self.__1, self.__2})))


def doctests() -> None:
    """
    >>> pair = UnorderedPair('A', 'B')

    >>> pair
    UnorderedPair('A', 'B')
    >>> ~pair
    UnorderedPair('B', 'A')
    >>> pair[0]
    'A'
    >>> pair[1]
    'B'
    >>> pair == ~pair
    True
    >>> pair != UnorderedPair('A', 'A')
    True
    >>> hash(pair) == hash(~pair)
    True
    >>> list(iter(pair))      # Insertion Order
    ['A', 'B']
    >>> list(reversed(pair))  # Reverse Insertion Order
    ['B', 'A']
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
