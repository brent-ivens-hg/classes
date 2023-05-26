from collections.abc import MutableSet, Sequence, Iterable


class OrderedSet(MutableSet):
    """
    A set that preserves insertion order by internally using a dict
    """

    def __init__(self, iterable: Iterable | None = None):
        self._map = {} if iterable is None else dict.fromkeys(iterable)

    def __contains__(self, item) -> bool:
        return item in self._map

    def __eq__(self, other) -> bool:
        return isinstance(other, (Sequence, OrderedSet)) and list(self) == list(other)

    def __invert__(self):
        return OrderedSet(reversed(self._map))

    def __iter__(self) -> iter:
        return iter(self._map)

    def __len__(self) -> int:
        return len(self._map)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({list(self) or ""})'

    def __reversed__(self) -> reversed:
        return reversed(self._map)

    def add(self, item) -> None:
        self._map[item] = None

    def discard(self, item) -> None:
        self._map.pop(item, None)

    difference, difference_update = MutableSet.__sub__, MutableSet.__isub__
    intersection, intersection_update = MutableSet.__and__, MutableSet.__iand__
    issubset, issuperset = MutableSet.__le__, MutableSet.__ge__
    symmetric_difference, symmetric_difference_update = MutableSet.__xor__, MutableSet.__ixor__
    union, update = MutableSet.__or__, MutableSet.__ior__


def doctest_ordered_set() -> None:
    """
    >>> A = OrderedSet('abracadabra')
    >>> B = OrderedSet('simsalabim')
    >>> A | B
    OrderedSet(['a', 'b', 'r', 'c', 'd', 's', 'i', 'm', 'l'])
    >>> A & B
    OrderedSet(['a', 'b'])
    >>> A - B
    OrderedSet(['r', 'c', 'd'])
    >>> A ^ B
    OrderedSet(['r', 'c', 'd', 's', 'i', 'm', 'l'])
    >>> A == B
    False
    >>> A != B
    True
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
