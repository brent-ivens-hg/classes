"""
Iter Help
"""
from abc import ABC, abstractmethod
from collections.abc import Iterator, Reversible
from typing import overload, Protocol, runtime_checkable, TypeVar
# LOCAL #
from utils.missing import MISSING

__all__ = ['MemoryIteratorBase', 'SupportsCurr', 'SupportsNext', 'SupportsPrev', 'curr', 'exhaust', 'prev']


_T = TypeVar('_T')
_VT = TypeVar('_VT')


# noinspection DuplicatedCode
@runtime_checkable
class SupportsCurr(Protocol[_T]):
    """An ABC with one abstract method __curr__."""
    __slots__ = ()

    @abstractmethod
    def __curr__(self) -> _T:
        pass


@runtime_checkable
class SupportsNext(Protocol[_T]):
    """An ABC with one abstract method __next__."""
    __slots__ = ()

    @abstractmethod
    def __next__(self) -> _T:
        pass


@runtime_checkable
class SupportsPrev(Protocol[_T]):
    """An ABC with one abstract method __prev__."""
    __slots__ = ()

    @abstractmethod
    def __prev__(self) -> _T:
        pass


class MemoryIteratorBase(ABC, Iterator[_T], SupportsCurr[_T], SupportsPrev[_T], Reversible[_T]):
    """An ABC with four abstract methods __prev__, __curr__, __next__ and __reversed__."""
    __slots__ = ()


@overload
def curr(iterator: SupportsCurr[_T]) -> _T:
    pass


@overload
def curr(iterator: SupportsCurr[_T], default: _VT = ...) -> _T | _VT:
    pass


def curr(iterator: SupportsCurr[_T], default: _VT = MISSING) -> _T | _VT:
    try:
        if not isinstance(iterator, SupportsCurr):
            raise AttributeError(f"{type(iterator).__name__!r} object has no attribute '__curr__'.")
        return iterator.__curr__()
    except StopIteration as e:
        if default is not MISSING:
            return default
        raise StopIteration(e) from None


@overload
def prev(iterator: SupportsPrev[_T]) -> _T:
    pass


@overload
def prev(iterator: SupportsPrev[_T], default: _VT = ...) -> _T | _VT:
    pass


def prev(iterator: SupportsPrev[_T], default: _VT = MISSING) -> _T | _VT:
    try:
        if not isinstance(iterator, SupportsPrev):
            raise AttributeError(f"{type(iterator).__name__!r} object has no attribute '__prev__'.")
        return iterator.__prev__()
    except StopIteration as e:
        if default is not MISSING:
            return default
        raise StopIteration(e) from None


def exhaust(iterator: Iterator[_T]) -> None:
    for _ in iterator:
        pass
