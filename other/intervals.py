"""
Intervals
"""
from collections.abc import Iterable
from math import inf


class Interval:
    """ Discrete Closed Interval """

    def __init__(self, start: int = -inf, stop: int = +inf) -> None:
        if type(start) != int: raise TypeError('invalid start')
        if type(stop)  != int: raise TypeError('invalid stop')
        if start > stop:       raise ValueError('start > stop')
        self.__start = start
        self.__stop = stop

    @property
    def start(self) -> int:
        return self.__start

    @property
    def stop(self) -> int:
        return self.__stop

    def __repr__(self):
        return f'{self.__class__.__name__}{self.start, self.stop}'

    def __str__(self):
        return f'[{self.start}..{self.stop}]'

    def __iter__(self):
        return iter(range(self.start, self.stop + 1))

    def __contains__(self, item):
        return self.start <= item <= self.stop

    def __eq__(self, other):
        other = self.cast(other)
        return (self.start, self.stop) == (other.start, other.stop)

    def __lt__(self, other):
        other = self.cast(other)
        return self.start < other.start

    def __le__(self, other):
        other = self.cast(other)
        return self < other or self == other

    def __gt__(self, other):
        other = self.cast(other)
        return self.stop > other.stop

    def __ge__(self, other):
        other = self.cast(other)
        return self > other or self == other

    def __or__(self, other):
        other = self.cast(other)
        if not self.overlaps(other): raise ValueError("intervals don't overlap")
        return Interval(min(self.start, other.start), max(self.stop, other.stop))

    def __and__(self, other):
        other = self.cast(other)
        if not self.overlaps(other): raise ValueError("intervals don't overlap")
        return Interval(max(self.start, other.start), min(self.stop, other.stop))

    def __lshift__(self, other):
        other = self.cast(other)
        if not self.overlaps(other): raise ValueError("intervals don't overlap")
        return Interval(self.start, other.start) if self < other else Interval(other.stop, self.stop)

    __rshift__ = lambda self, other: other << self
    __matmul__ = __rmatmul__ = lambda self, other: self.overlaps(other)
    __mod__ = __rmod__ = isdisjoint = lambda self, other: not self.overlaps(other)

    union = lambda self, other: self | other
    intersection = lambda self, other: self & other

    def overlaps(self, other) -> bool:
        other = self.cast(other)
        return self.start <= other.stop and other.start <= self.stop

    @classmethod
    def cast(cls, other: 'Interval | Iterable[int]') -> 'Interval':
        if isinstance(other, cls):
            return other
        try:
            return cls.from_iterable(other)
        except (AttributeError, TypeError, ValueError):
            raise RuntimeError(f"couldn't cast {other!r} to {cls.__name__!r}") from None

    @classmethod
    def from_iterable(cls, iterable: Iterable[int]) -> 'Interval':
        return cls(*iterable)


# def test_functions():
#     X = Interval(0, 2)
#     Y = Interval(1, 3)
#     print('\tX\t\tY')
#     print(' ', X, Y)
#     print('U', X | Y, Y | X, X.union(Y))
#     print('I', X & Y, Y & X, X.intersection(Y))
#     print('L', X << Y, Y << X)
#     print('R', X >> Y, Y >> X)
#     print(X @ Y, Y @ X)  # overlap
#     print(X % Y, Y % X)  # don't overlap
#     print(X < Y, Y > X)  # smaller
#     print(X > Y, Y < X)  # greater
#     for x in Interval(-2, 0) | Interval(0, 2):
#         print(x)


class Union(list):
    def __init__(self, seq):
        it = iter(sorted(seq))
        I = Interval.cast(next(it))
        for J in it:
            J = Interval.cast(J)
            if I @ J:
                I |= J
            else:
                self.append(I)
                I = J
        self.append(I)

    def __repr__(self):
        return f'{self.__class__.__name__}({super().__repr__()})'

    def __str__(self):
        return ' U '.join(map(str, super().__iter__()))

    def __iter__(self):
        return (j for i in super().__iter__() for j in i)


def test_union():
    U = Union([Interval(0, 1), Interval(2, 3), Interval(3, 5)])
    print(U)
    print(list(U))
    U = Union([Interval(0, 1), Interval(2, 3), Interval(4, 5)])
    print(U)
    print(list(U))
