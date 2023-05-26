"""
Unordered Integers
"""
from math import prod
from collections.abc import Sequence


def prime_hash(n: int, primes: Sequence[int] = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)) -> int:
    """
    Hash for numbers with same digits.

    >>> prime_hash(135451)
    117117

    >>> [prime_hash(i) for i in range(15)]
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 6, 9, 15, 21, 33]

    >>> [i for i in range(10 ** 5) if i == prime_hash(i)]  # A115078
    [171, 290, 2145, 3381, 74613]
    """
    return prod(primes[int(d)] for d in str(n))


class UnorderedInteger(int):
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.real})'

    def __str__(self) -> str:
        return str(self.real)

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)

    def __hash__(self) -> int:
        if not hasattr(self, '_hash'):
            self._hash = prime_hash(self)
        return self._hash


def doctest_unordered_integer() -> None:
    """
    >>> a = UnorderedInteger(13)
    >>> b = UnorderedInteger(31)
    >>> a
    UnorderedInteger(13)
    >>> b
    UnorderedInteger(31)
    >>> a == b
    True
    >>> hash(a)
    21
    >>> hash(a) == hash(b)
    True
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
