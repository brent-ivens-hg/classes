"""
Binary Heaps
"""
from __future__ import annotations

from collections import deque
from collections.abc import Iterable, Generator
from dataclasses import dataclass
from itertools import count, islice
from typing import TypeVar, Generic

_T = TypeVar('_T')


def binary_heap_levels(iterable: Iterable) -> Generator:
    """
    Visualize Binary Tree Levels

    >>> list(binary_heap_levels('123456789ABCDEF'))
    [('1',), ('2', '3'), ('4', '5', '6', '7'), ('8', '9', 'A', 'B', 'C', 'D', 'E', 'F')]
    >>> list(binary_heap_levels([1, 2, 3, 4, 5, 6, 7, 8, 9]))
    [(1,), (2, 3), (4, 5, 6, 7), (8, 9)]
    """
    it = iter(iterable)
    for n in count():
        chunk = tuple(islice(it, 1 << n))
        if not chunk:
            return
        yield chunk


@dataclass
class Node(Generic[_T]):
    value: _T
    left: Node = None
    right: Node = None

    def __repr__(self) -> str:
        res = [str(self.value)]
        if self.left: res.append(f'left={self.left}')
        if self.right: res.append(f'right={self.right}')
        return '%s(%s)' % (self.__class__.__name__, ', '.join(res))

    def insert(self, value: _T) -> None:
        """
        Breadth First/Level Order Insertion
        """
        if not self.value:
            self.value = value
            return
        queue = deque([self])
        while queue:
            node = queue.popleft()
            if node.left is None:
                node.left = Node(value)
                return
            else:
                queue.append(node.left)
            if node.right is None:
                node.right = Node(value)
                return
            else:
                queue.append(node.right)


class BinHeap(Node[_T]):
    @classmethod
    def from_iterable(cls, iterable: Iterable[_T]):
        it = iter(iterable)
        root = next(it)
        res = BinHeap(root)
        for value in it:
            res.insert(value)
        return res

    def is_min_heap(self, verbose: bool = False) -> bool:
        """
        All nodes are either less than or equal to each of its children
        """
        if not self.value:
            return True
        queue: deque[Node] = deque([self])
        while queue:
            node = queue.popleft()
            if node.left is not None:
                if node.value > node.left.value:
                    if verbose: print(f'{node.value} must be <= than {node.left.value}')
                    return False
                queue.append(node.left)
            if node.right is not None:
                if node.value > node.right.value:
                    if verbose: print(f'{node.value} must be <= than {node.right.value}')
                    return False
                queue.append(node.right)
        if verbose: print('heap is min-heap')
        return True

    def is_max_heap(self, verbose: bool = False) -> bool:
        """
        All nodes are either greater than or equal to each of its children
        """
        if not self.value:
            return True
        queue: deque[Node] = deque([self])
        while queue:
            node = queue.popleft()
            if node.left is not None:
                if node.value < node.left.value:
                    if verbose: print(f'{node.value} must be >= than {node.left.value}')
                    return False
                queue.append(node.left)
            if node.right is not None:
                if node.value < node.right.value:
                    if verbose: print(f'{node.value} must be >= than {node.right.value}')
                    return False
                queue.append(node.right)
        if verbose: print('heap is max-heap')
        return True


def doctest_bin_heap() -> None:
    """
    >>> seq = [1, 2, 4, 7, 3, 6, 9, 5, 8]
    >>> bin_heap = list(binary_heap_levels(seq))
    >>> bin_heap
    [(1,), (2, 4), (7, 3, 6, 9), (5, 8)]
    >>> BinHeap.from_iterable(seq).is_min_heap(verbose=True)
    7 must be <= than 5
    False
    >>> BinHeap.from_iterable(seq).is_max_heap(verbose=True)
    1 must be >= than 2
    False
    >>> seq = 10, 14, 19, 26, 31, 42, 27, 44, 35, 33
    >>> heap = BinHeap.from_iterable(seq)
    >>> heap.is_min_heap(verbose=True)
    heap is min-heap
    True
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
