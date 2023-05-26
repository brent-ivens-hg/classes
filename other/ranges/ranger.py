"""
ranger.py
"""
__all__ = ['Range', 'RangerException']

# noinspection SpellCheckingInspection
Rangeable = int | slice | tuple['Rangeable', ...] | None


class RangerException(Exception):
    pass


# Range ~ Ranged(list)
class Ranger:
    def __getitem__(self, item: Rangeable) -> list:
        match type(item).__name__:
            case 'int':
                return [item]
            case 'slice':
                return list(range(item.start or 0, item.stop or 0, item.step or 1))
            case 'tuple':
                res = []
                for x in item:
                    res.extend(self[x])
                return res
            case 'NoneType':
                return []
            case _:
                raise RangerException(f'invalid type: {type(item)!r}')


Range = Ranger()


def doctest_ranger() -> None:
    """
    >>> Range[10]
    [10]
    >>> Range[1:10]
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> Range[1, 10]  # Range[(1, 10)]
    [1, 10]
    >>> Range[0, 1:10]  # Range[(1, 1:10)]
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> Range[1::-1]
    [1]
    >>> Range[-1::1]
    [-1]
    >>> Range[4, 5:-5:-2]
    [4, 5, 3, 1, -1, -3]
    >>> Range[1, (2, (3, (4, (5,))))]
    [1, 2, 3, 4, 5]

    >>> Range[]
    Traceback (most recent call last):
    SyntaxError: invalid syntax. Perhaps you forgot a comma?
    >>> Range[:]
    []
    >>> Range[::]
    []
    >>> Range[None]
    []
    >>> Range[None:None]
    []
    >>> Range[None:None:None]
    []

    >>> Range[5] + Range[5]
    [5, 5]
    >>> Range[5] * 5
    [5, 5, 5, 5, 5]
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
