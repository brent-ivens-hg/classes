"""
Iterators
"""
from collections.abc import Callable, Generator, Iterable, Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar
# LOCAL #
from classes.iters.tools import MemoryIteratorBase, curr, prev

__all__ = ['Defaulter', 'DefaultCaller', 'MemoryIterator']

_T = TypeVar('_T')
_VT = TypeVar('_VT')


class Defaulter(Iterator[_T | _VT]):
    """
    Yields default value when iterator is exhausted

    >>> it = Defaulter([1, 2, 3], default=0)
    >>> [next(it) for _ in range(5)]
    [1, 2, 3, 0, 0]
    """

    def __init__(self, iterable: Iterable[_T], default: _VT = None) -> None:
        self._iter = iter(iterable)
        self._default = default

    @property
    def default(self) -> _VT:
        return self._default

    def __next__(self) -> _T | _VT:
        return next(self._iter, self.default)


class DefaultCaller(Iterator[_T | _VT]):
    """
    Calls default value and yields it when iterator is exhausted

    >>> it = DefaultCaller([1, 2, 3], default=lambda: 0)
    >>> [next(it) for _ in range(5)]
    [1, 2, 3, 0, 0]
    >>> # Similar to
    >>> it = iter(lambda: 0, True)
    >>> [next(it) for _ in range(5)]
    [0, 0, 0, 0, 0]
    """

    def __init__(self, iterable: Iterable[_T], default: Callable[[], _VT] = lambda: None) -> None:
        self._iter = iter(iterable)
        self._default = default

    @property
    def default(self) -> _VT:
        return self._default()

    def __next__(self) -> _T | _VT:
        return next(self._iter, self.default)


@dataclass
class Node(Generic[_T]):
    value: _T
    previous: _T = None
    next: _T = None


class MemoryIterator(MemoryIteratorBase):
    """
    Iterator that remembers the previous iteration
    accessible with curr({__curr__})  and allows rollback with prev({__prev__}).
    """

    def __init__(self, iterable: Iterable[_T]) -> None:
        self._node: Node[_T] | None = None  # Linked List
        self._iter: Iterator[_T] = iter(iterable)

    def _next_node(self) -> Node[_T]:
        return Node(next(self._iter), previous=self._node)

    def __next__(self) -> _T:
        if self._node is None:
            self._node = self._next_node()
            return self._node.value
        if self._node.next is None:
            self._node.next = self._next_node()
        self._node = self._node.next
        return self._node.value

    def __curr__(self) -> _T:
        if self._node is None:
            raise StopIteration
        return self._node.value

    def __prev__(self) -> _T:
        self._node = self._node
        if self._node is None or self._node.previous is None:
            raise StopIteration
        self._node = self._node.previous
        return self._node.value

    def __iter__(self) -> 'MemoryIterator[_T]':
        # TODO: return a NEW memory-iterator
        # WARN: DON'T mutate 'self' !
        raise NotImplementedError

    def __reversed__(self) -> 'MemoryIterator[_T]':
        # TODO: return a NEW reversed memory-iterator: https://www.codewars.com/kata/52f6be83172a8ba0be000342
        # WARN: DON'T mutate 'self' !
        raise NotImplementedError

    def rollback(self) -> Generator[_T, None, None]:  # WARN: mutates self
        try:
            yield curr(self)
            while True:
                yield prev(self)
        except StopIteration:
            pass


def doctests() -> None:
    """
    Overview
    --------
    >>> it = MemoryIterator([1, 2, 3])
    >>> prev(it, 'no previous value')   # iterator hasn't been initialized -> no value to return to
    'no previous value'
    >>> curr(it, 'no current value')
    'no current value'

    >>> next(it)
    1
    >>> next(it)
    2
    >>> next(it)
    3
    >>> curr(it)
    3
    >>> prev(it)
    2
    >>> prev(it)
    1

    >>> prev(it)
    Traceback (most recent call last):
    StopIteration

    >>> mit = MemoryIterator(range(10))

    >>> it = iter(mit)              # setup
    >>> next(it)                    # consume one
    0
    >>> list(it)                    # consume all
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> curr(it)
    9

    # TODO: implement
    # >>> it = reversed(mit)          # setup
    # >>> next(it)                    # consume one
    # 9
    # >>> list(it)                    # consume all
    # [8, 7, 6, 5, 4, 3, 2, 1, 0]
    # >>> curr(it)
    # 0
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
