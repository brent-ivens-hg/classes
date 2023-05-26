from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable, Iterable
from operator import lt, gt, ne, eq
from typing import Generic, TypeVar

_T = TypeVar('_T')


class Generizer(Generic[_T]):
    """
    Holds on to a value determined by the (abstract) operator
    """

    def __init__(self, value: _T):
        self.__value = value
        self.__type = type(value)

    @property
    @abstractmethod
    def operator(self) -> Callable[[_T, _T], bool]:
        ...

    def value(self) -> _T:
        return self.__value

    def add(self, value: _T) -> None:
        if type(value) != self.__type:
            raise TypeError(f'\'add\' not supported between instances of '
                            f'{self.__type.__name__!r} and {type(value).__name__!r}')

        if self.operator(value, self.__value):
            self.__value = value

    def add_all(self, *values: _T) -> None:
        for value in values:
            self.add(value)

    @classmethod
    def from_iterable(cls, iterable: Iterable[_T]) -> Generizer[_T]:
        it = iter(iterable)
        generizer = cls(next(it))
        generizer.add_all(*it)
        return generizer


class Maximizer(Generizer):
    """
    Keeps maximum value

    >>> maximizer = Maximizer(1.5)
    >>> maximizer.add(1.0)
    >>> maximizer.add(3.0)
    >>> maximizer.add(-0.2)
    >>> maximizer.value()
    3.0
    >>> maximizer = Maximizer('apple')
    >>> maximizer.add_all('pear', 'banana', 'orange')
    >>> maximizer.value()
    'pear'
    >>> Maximizer.from_iterable([0, 1, 3, 2]).value()
    3
    """
    operator = gt


class Minimizer(Generizer):
    """
    Keeps minimum value

    >>> minimizer = Minimizer(1.5)
    >>> minimizer.add(1.0)
    >>> minimizer.add(3.0)
    >>> minimizer.add(-0.2)
    >>> minimizer.value()
    -0.2
    >>> minimizer = Minimizer('apple')
    >>> minimizer.add_all('pear', 'banana', 'orange')
    >>> minimizer.value()
    'apple'
    >>> Minimizer.from_iterable([-0, -1, -3, -2]).value()
    -3
    """
    operator = lt


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    Novelizer = type('priorizer', (Generizer,), {'operator': ne})
    # noinspection PyUnresolvedReferences
    print(Novelizer.from_iterable([0, 1, 2, 3, 3]).value())  # takes last unequal value (2nd to last 3)

    Priorizer = type('priorizer', (Generizer,), {'operator': eq})
    # noinspection PyUnresolvedReferences
    print(Priorizer.from_iterable([0, 0, 1, 2, 3]).value())  # takes last equal value (2nd 0)
