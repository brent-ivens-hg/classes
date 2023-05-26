"""
Ascii Range
"""
from collections import deque
from collections.abc import Iterable
from re import compile

RANGE = compile('(.)(?:-(.))?')


def consecutive(p: tuple, q: tuple) -> bool:
    return ord(p[1]) == ord(q[0]) - 1


def overlap(p: tuple, q: tuple) -> bool:
    return p[0] <= q[0] <= p[1]


def merge(p: tuple, q: tuple) -> tuple:
    p_start, p_stop = p
    q_start, q_stop = q
    return min(p_start, q_start), max(p_stop, q_stop)


def merged(iterable: Iterable) -> list:
    queue = deque(iterable)
    res = []
    a = queue.popleft()
    while queue:
        b = queue.popleft()
        if overlap(a, b) or consecutive(a, b):
            a = merge(a, b)
        else:
            res.append(a)
            a = b
    res.append(a)
    return res


class AsciiRangeException(Exception):
    pass


class AsciiRange:
    def __init__(self, string: str) -> None:
        ranges = (m.groups() for m in RANGE.finditer(string))
        ranges = sorted((from_, from_) if to is None else (from_, to) for from_, to in ranges)
        if any(a > b for a, b in ranges):
            raise AsciiRangeException('Illegal character range (to < from)')
        self.ranges = merged(ranges)

    def __repr__(self) -> str:
        return '{}({!r})'.format(self.__class__.__name__,
                                 ''.join(a if a == b else '-'.join([a, b]) for a, b in self.ranges))

    def __str__(self) -> str:
        return ''.join(iter(self))

    def __iter__(self) -> iter:
        for a, b in self.ranges:
            for i in range(ord(a), ord(b) + 1):
                yield chr(i)

    def __reversed__(self) -> reversed:
        for a, b in reversed(self.ranges):
            for i in range(ord(b), ord(a) - 1, -1):
                yield chr(i)

    def __contains__(self, char: str) -> bool:
        if not (isinstance(char, str) and len(char) == 1):
            raise AsciiRangeException('Invalid character')
        return any(char == a if b == '' else a <= char <= b for a, b in self.ranges)


def doctest_ascii_range() -> None:
    """
    >>> arange = AsciiRange('a-zA-Z0-9')
    >>> arange
    AsciiRange('0-9A-Za-z')
    >>> print(arange)
    0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
    >>> next(iter(arange))
    '0'
    >>> ''.join(reversed(arange))
    'zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA9876543210'
    >>> 'a' in arange
    True
    >>> '%' in arange
    False

    >>> AsciiRange('A-A')
    AsciiRange('A')
    >>> AsciiRange('ABCDE')
    AsciiRange('A-E')
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
