"""
Infix Notation
"""
from collections.abc import Callable
from functools import partial
from inspect import signature, Parameter
from typing import TypeVar

_T = TypeVar('_T')
_S = TypeVar('_S')


# noinspection SpellCheckingInspection,PyUnresolvedReferences
def argcount(function: Callable) -> int:
    return function.__code__.co_argcount


def fixable(function: Callable) -> bool:
    # POSITIONAL_ONLY        [v]
    # POSITIONAL_OR_KEYWORD  [v]
    # VAR_POSITIONAL         [x]
    # KEYWORD_ONLY           [x]
    # VAR_KEYWORD            [x]
    return callable(function) and all(
        p.kind in {Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD}
        for p in signature(function).parameters.values()
    )


class Prefix:
    def __init__(self, n_ary_operator: Callable[..., _S] | partial[_T, _S]) -> None:
        assert fixable(n_ary_operator) and argcount(n_ary_operator) > 0, 'invalid n-ary operator'
        self._n_ary_operator = n_ary_operator

    def __or__(self, operand: _T) -> _S:
        if argcount(self._n_ary_operator) == 1:
            return self._n_ary_operator(operand)
        return Prefix(partial(self._n_ary_operator, operand))


class Infix:
    def __init__(self, binary_operator: Callable[[_T, _T], _S] | partial[_T, _S]) -> None:
        assert (fixable(binary_operator) and
                len(binary_operator.args) == 1 and argcount(binary_operator) == 1
                if isinstance(binary_operator, partial) else
                argcount(binary_operator) == 2), 'invalid binary operator'
        self._binary_operator = binary_operator

    def __or__(self, right_operand: _T) -> _S:
        return self._binary_operator(right_operand)

    def __ror__(self, left_operand: _T) -> 'Infix':
        return Infix(partial(self._binary_operator, left_operand))


class Postfix:
    def __init__(self, n_ary_operator: Callable[..., _S] | partial[_T, _S]) -> None:
        assert fixable(n_ary_operator) and argcount(n_ary_operator) > 0, 'invalid n-ary operator'
        self._n_ary_operator = n_ary_operator

    def __ror__(self, operand: _T) -> _S:
        if argcount(self._n_ary_operator) == 1:
            return self._n_ary_operator(operand)
        return Postfix(partial(self._n_ary_operator, operand))


def doctest_infix() -> None:
    """
    >>> from logical.gates.unary import *
    >>> from logical.gates.binary import *

    >>> not_ = Prefix(NOT)
    >>> not_ | 0
    1
    >>> not_ | 1
    0
    >>> and_ = Infix(AND)
    >>> 0 | and_ | 0
    0
    >>> 0 | and_ | 1
    0
    >>> 1 | and_ | 0
    0
    >>> 1 | and_ | 1
    1

    >>> or_ = Infix(OR)
    >>> 0 | or_ | 0
    0
    >>> 0 | or_ | 1
    1
    >>> 1 | or_ | 0
    1
    >>> 1 | or_ | 1
    1

    >>> xor = Infix(XOR)
    >>> 0 | xor | 0
    0
    >>> 0 | xor | 1
    1
    >>> 1 | xor | 0
    1
    >>> 1 | xor | 1
    0

    >>> add3 = Prefix(lambda a, b, c: a + b + c)
    >>> add3 | 1 | 2 | 3
    6

    >>> add_one = Postfix(lambda x: x + 1)
    >>> 0 | add_one
    1

    >>> import operator as op

    >>> plus       = Infix(op.add)
    >>> minus      = Infix(op.sub)
    >>> times      = Infix(op.mul)
    >>> divided_by = Infix(op.floordiv)
    >>> raised_by  = Infix(op.pow)
    >>> root       = Infix(lambda x, y: round(x ** (1 / y)))

    >>> (5 | plus | (9 | root | 2)) | times | 2 | minus | 7 | divided_by | 3 | raised_by | 2
    9
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
