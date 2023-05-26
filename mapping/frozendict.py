"""
Frozen Dictionary
"""
from collections import abc
from typing import Hashable, NoReturn, TypeVar, final

__all__ = ['frozendict']

_T = TypeVar('_T')
_S = TypeVar('_S')

_KT = TypeVar('_KT')
_VT = TypeVar('_VT')


# noinspection PyPep8Naming
class _frozendict_keys(abc.KeysView[_KT]):
    def __repr__(self) -> str:
        return f'frozendict_keys({list(self)})'


# noinspection PyPep8Naming
class _frozendict_values(abc.ValuesView[_VT]):
    def __repr__(self) -> str:
        return f'frozendict_values({list(self)})'


# noinspection PyPep8Naming
class _frozendict_items(abc.ItemsView[_KT, _VT]):
    def __repr__(self) -> str:
        return f'frozendict_items({list(self)})'


# noinspection PyPep8Naming
@final
class frozendict(abc.Mapping[_KT, _VT], Hashable):
    """
    Immutable (and Hashable) wrapper for dictionaries
    """

    def __init__(self, *args, **kwargs) -> None:
        self.__dict = dict(*args, **kwargs)  # internal dictionary

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.__dict!r})'

    def __iter__(self) -> abc.Iterator[_KT]:
        return iter(self.__dict)

    def __len__(self) -> int:
        return len(self.__dict)

    def __hash__(self) -> int:
        if not hasattr(self, '_hash'):
            # noinspection PyProtectedMember
            self._hash = super().items()._hash()
        return self._hash

    def __getitem__(self, key: _KT) -> _VT:
        return self.__dict[key]

    def __or__(self, other: abc.Mapping[_KT, _VT]) -> 'frozendict[_KT, _VT]':
        if isinstance(other, frozendict): other = other.__dict
        return frozendict(self, **other)

    def __ior__(self, other: abc.Mapping[_KT, _VT]) -> NoReturn:
        raise TypeError(f'unsupported operand type(s) for |=: {self.__class__.__name__} and {other.__class__.__name__}')

    def __ror__(self, other: abc.Mapping[_KT, _VT]) -> abc.Mapping[_KT, _VT]:
        return other | self.__dict

    def keys(self) -> _frozendict_keys[_KT]:
        return _frozendict_keys(self)

    def values(self) -> _frozendict_values[_VT]:
        return _frozendict_values(self)

    def items(self) -> _frozendict_items[_KT, _VT]:
        return _frozendict_items(self)

    def copy(self) -> 'frozendict[_KT, _VT]':
        """ :returns: a shallow copy """
        return frozendict(self)

    @classmethod
    def fromkeys(cls, iterable: abc.Iterable[_T], value: _S | None = None) -> 'frozendict[_T, _S | None]':
        """ Create a new frozen-dictionary with keys from iterable and values set to value. """
        return cls(dict.fromkeys(iterable, value))


# noinspection All
def _doctest_frozendict() -> None:
    """
    >>> f1 = frozendict({'apples': 1, 'bananas': 2})
    >>> f1
    frozendict({'apples': 1, 'bananas': 2})
    >>> f1['apples']
    1
    >>> f1.get('bananas')
    2
    >>> f1.get('mangoes')
    >>> f2 = frozendict({'bananas': 3, 'mangoes': 5})
    >>> f2
    frozendict({'bananas': 3, 'mangoes': 5})
    >>> # dict_views
    >>> f1.keys()
    frozendict_keys(['apples', 'bananas'])
    >>> f1.values()
    frozendict_values([1, 2])
    >>> f2.items()
    frozendict_items([('bananas', 3), ('mangoes', 5)])
    >>> # pow(frozendict, frozendict): merge frozendicts
    >>> f1 | f2
    frozendict({'apples': 1, 'bananas': 3, 'mangoes': 5})
    >>> # fromkeys
    >>> frozendict.fromkeys('abc', 0)
    frozendict({'a': 0, 'b': 0, 'c': 0})
    >>> # frozendict as dict-key
    >>> d1 = {f1: 'salad'}
    >>> d1[f1]
    'salad'
    >>> frozendict(a=1) | dict(b=2)
    frozendict({'a': 1, 'b': 2})
    >>> dict(b=2) | frozendict(a=1)
    {'b': 2, 'a': 1}
    >>> # immutability tests
    >>> f3 = frozendict(a=1)
    >>> f3.__getitem__('a')  # no false positives
    1
    >>> f3.__setitem__('b', 2)
    Traceback (most recent call last):
    AttributeError: 'frozendict' object has no attribute '__setitem__'
    >>> f3.__delitem__('a')
    Traceback (most recent call last):
    AttributeError: 'frozendict' object has no attribute '__delitem__'
    >>> f3.pop('a')
    Traceback (most recent call last):
    AttributeError: 'frozendict' object has no attribute 'pop'
    >>> f3.popitem()
    Traceback (most recent call last):
    AttributeError: 'frozendict' object has no attribute 'popitem'
    >>> f3.setdefault('b', 2)
    Traceback (most recent call last):
    AttributeError: 'frozendict' object has no attribute 'setdefault'
    >>> f3.update(b=2)
    Traceback (most recent call last):
    AttributeError: 'frozendict' object has no attribute 'update'
    >>> f3.clear()
    Traceback (most recent call last):
    AttributeError: 'frozendict' object has no attribute 'clear'
    >>> dict.update(f3, b=2)
    Traceback (most recent call last):
    TypeError: descriptor 'update' for 'dict' objects doesn't apply to a 'frozendict' object
    >>> dict.setdefault(f3, 'b', 2)
    Traceback (most recent call last):
    TypeError: descriptor 'setdefault' for 'dict' objects doesn't apply to a 'frozendict' object
    >>> dict.clear(f3)
    Traceback (most recent call last):
    TypeError: descriptor 'clear' for 'dict' objects doesn't apply to a 'frozendict' object
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
else:
    import warnings

    warnings.warn(
        "'frozendict' is for demonstrative purposes only, use 'types.MappingProxyType' instead",
        ImportWarning
    )
