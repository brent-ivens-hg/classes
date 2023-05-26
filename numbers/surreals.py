"""
Surreal Objects: https://en.wikipedia.org/wiki/Surreal_number
"""
from math import isinf

pos_inf = float('inf')
neg_inf = float('-inf')


class Infinite:
    """
    Infinite Object
    """

    def __init__(self, positive: bool = True) -> None:
        self.positive = positive

    def __neg__(self) -> 'Infinite':
        return Infinite(not self.positive)

    def __eq__(self, other) -> bool:
        if isinstance(other, Infinite):
            return self.positive == other.positive
        return other == pos_inf if self.positive else other == neg_inf

    def __lt__(self, other) -> bool:
        if self == other:
            return False
        return not self.positive

    def __gt__(self, other) -> bool:
        if self == other:
            return False
        return self.positive

    def __le__(self, other) -> bool:
        return self == other or not self.positive

    def __ge__(self, other) -> bool:
        return self == other or self.positive

    def __bool__(self) -> bool:
        return True

    @staticmethod
    def __nonzero__() -> bool:
        return True

    def __float__(self) -> float:
        return pos_inf if self.positive else neg_inf

    def __add__(self, other) -> 'Infinite':
        if isinf(other) and other != self:
            return NotImplemented
        return self

    def __radd__(self, other) -> 'Infinite':
        return self

    def __sub__(self, other) -> 'Infinite':
        if isinf(other) and other == self:
            return NotImplemented
        return self

    def __rsub__(self, other) -> 'Infinite':
        return self

    @staticmethod
    def timetuple() -> tuple:
        return tuple()

    def __abs__(self) -> 'Infinite':
        return Infinite()

    def __pos__(self) -> 'Infinite':
        return self

    def __truediv__(self, other) -> 'Infinite':
        if isinf(other):
            return NotImplemented
        return Infinite(other > 0 and self.positive or other < 0 and not self.positive)

    def __rtruediv__(self, other) -> int:
        return 0

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(positive={self.positive})'

    def __str__(self):
        return ''

    __floordiv__ = __truediv__
    __rfloordiv__ = __rtruediv__

    def __mul__(self, other) -> 'Infinite':
        if other == 0:
            return NotImplemented
        return Infinite(other > 0 and self.positive or other < 0 and not self.positive)

    __rmul__ = __mul__

    def __pow__(self, other) -> 'Infinite' or float:
        if other == 0:
            return NotImplemented
        if other == -self:
            return -0.0 if not self.positive else 0.0
        return Infinite()

    def __rpow__(self, other) -> 'Infinite' or float:
        if other in (1, -1):
            return NotImplemented
        elif other == -self:
            return -0.0 if not self.positive else 0.0
        else:
            return Infinite()

    def __hash__(self) -> int:
        return hash((Infinite, self.positive))


inf = Infinite()


def doctest_infinite() -> None:
    """
    >>> # repr of inf
    >>> inf
    Infinite(positive=True)
    >>> -inf
    Infinite(positive=False)

    >>> # comparison: 0 & inf
    >>> 0 < inf
    True
    >>> 0 <= inf
    True
    >>> 0 > inf
    False
    >>> 0 >= inf
    False
    >>> # comparison: 0 & -inf
    >>> 0 < -inf
    False
    >>> 0 <= -inf
    False
    >>> 0 > -inf
    True
    >>> 0 >= -inf
    True

    >>> inf + 0, 0 + inf
    (Infinite(positive=True), Infinite(positive=True))
    >>> inf + 1, 1 + inf
    (Infinite(positive=True), Infinite(positive=True))
    >>> inf + -1, -1 + inf
    (Infinite(positive=True), Infinite(positive=True))
    >>> inf + inf, -inf + -inf
    (Infinite(positive=True), Infinite(positive=False))
    >>> inf + -inf, -inf + inf
    Traceback (most recent call last):
    TypeError: unsupported operand type(s) for +: 'Infinite' and 'Infinite'

    >>> inf - 0, 0 - inf
    (Infinite(positive=True), Infinite(positive=True))
    >>> inf - 1, 1 - inf
    (Infinite(positive=True), Infinite(positive=True))
    >>> inf - -1, -1 - inf
    (Infinite(positive=True), Infinite(positive=True))
    >>> -inf - inf, inf - -inf
    (Infinite(positive=False), Infinite(positive=True))
    >>> inf - inf, -inf - -inf
    Traceback (most recent call last):
    TypeError: unsupported operand type(s) for -: 'Infinite' and 'Infinite'

    # >>> inf * 0
    # >>> inf * 1
    # >>> inf * -1
    # >>> inf * inf
    # >>> inf * -inf
    # >>> -inf * inf
    # >>> -inf * -inf
    # >>> 0 * inf
    # >>> 1 * inf
    # >>> -1 * inf
    #
    # >>> inf / 0
    # >>> inf / 1
    # >>> inf / -1
    # >>> inf / inf
    # >>> inf / -inf
    # >>> -inf / inf
    # >>> -inf / -inf
    # >>> 0 / inf
    # >>> 1 / inf
    # >>> -1 / inf
    #
    # >>> inf // 0
    # >>> inf // 1
    # >>> inf // -1
    # >>> inf // inf
    # >>> inf // -inf
    # >>> -inf // inf
    # >>> -inf // -inf
    # >>> 0 // inf
    # >>> 1 // inf
    # >>> -1 // inf
    #
    # >>> inf % 0
    # >>> inf % 1
    # >>> inf % -1
    # >>> inf % inf
    # >>> inf % -inf
    # >>> -inf % inf
    # >>> -inf % -inf
    # >>> 0 % inf
    # >>> 1 % inf
    # >>> -1 % inf
    #
    # >>> divmod(inf, 0)
    # >>> divmod(inf, 1)
    # >>> divmod(inf, -1)
    # >>> divmod(inf, inf)
    # >>> divmod(inf, -inf)
    # >>> divmod(-inf, inf)
    # >>> divmod(-inf, -inf)
    # >>> divmod(0, inf)
    # >>> divmod(1, inf)
    # >>> divmod(-1, inf)
    """


class Epsilon:  # TODO: https://stackoverflow.com/a/16819260
    """
    Infinitesimal Object: 0 < E < a / -a < -E < 0
    """

    def __init__(self, positive: bool = True) -> None:
        self.positive = positive

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(positive={self.positive})'

    def __neg__(self) -> 'Epsilon':
        return Epsilon(not self.positive)

    def __eq__(self, other) -> bool:
        return isinstance(other, Epsilon) and self.positive == other.positive

    def __lt__(self, other) -> bool:
        return other > 0 if self.positive else other >= 0

    def __gt__(self, other) -> bool:
        return other <= 0 if self.positive else other < 0

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __ge__(self, other) -> bool:
        return self > other or self == other


eps = Epsilon()


def doctest_epsilon() -> None:
    """
    >>> eps
    Epsilon(positive=True)

    >>> eps < -1  # Any neg
    False
    >>> eps < 0  # Zero
    False
    >>> eps < 1  # Any pos
    True

    >>> eps > -1  # Any neg
    True
    >>> eps > 0  # Zero
    True
    >>> eps > 1  # Any pos
    False

    >>> -eps < -1  # Any neg
    False
    >>> -eps < 0  # Zero
    True
    >>> -eps < 1  # Any pos
    True

    >>> -eps > -1  # Any neg
    True
    >>> -eps > 0  # Zero
    False
    >>> -eps > 1  # Any pos
    False
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
