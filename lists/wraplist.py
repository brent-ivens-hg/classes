"""
Wrapping List
"""
from typing import TypeVar

_T = TypeVar('_T')


class WrapList(list[_T]):
    """
    >>> lst = WrapList(range(10))
    >>> lst
    WrapList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> # getting
    >>> lst[100]
    0
    >>> # setting
    >>> lst[-7] = None
    >>> lst
    WrapList([0, 1, 2, None, 4, 5, 6, 7, 8, 9])
    >>> # deleting
    >>> del lst[5]
    >>> lst
    WrapList([0, 1, 2, None, 4, 6, 7, 8, 9])
    """

    def __repr__(self):
        return f'{self.__class__.__name__}({super().__repr__()})'

    def __getitem__(self, item: int | slice) -> _T:
        if isinstance(item, int):
            item %= len(self)
        return super().__getitem__(item)

    def __setitem__(self, key: int | slice, value: _T) -> None:
        if isinstance(key, int):
            key %= len(self)
        return super().__setitem__(key, value)

    def __delitem__(self, key: int | slice):
        if isinstance(key, int):
            key %= len(self)
        return super().__delitem__(key)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
