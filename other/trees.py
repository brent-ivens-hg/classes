"""
Trees
"""
from collections.abc import Generator
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Node:
    value: Any
    children: 'list[Node]' = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.children, list):
            raise TypeError(f'children must be of type {list}')
        if not all(isinstance(child, Node) for child in self.children):
            raise ValueError(f'every child must be of type {Node}')


@dataclass
class Tree:
    """
    Rooted Tree
    """
    root: Node

    def __post_init__(self) -> None:
        if self.root is None:
            raise ValueError('tree must contain a node')
        if not isinstance(self.root, Node):
            raise TypeError(f'root must be of type {Node}')


def preorder(tree: Tree) -> Generator[Node, None, None]:
    yield from preorder_recur(tree.root)


def preorder_recur(node: Node | None) -> Generator[Node, None, None]:
    yield node.value
    for child in node.children:
        yield from preorder_recur(child)


def postorder(tree: Tree) -> Generator[Node, None, None]:
    yield from postorder_recur(tree.root)


def postorder_recur(node: Node | None) -> Generator[Node, None, None]:
    for child in node.children:
        yield from postorder_recur(child)
    yield node.value


def height(tree: Tree) -> int:
    """
    :returns: distance to the furthest leaf
    """
    return height_recur(tree.root)


def height_recur(node: Node | None) -> int:
    return 1 + max(map(height_recur, node.children), default=0)


def doctests() -> None:
    """
    >>> t = Tree(Node(1, [
    ...     Node(2, [Node(3), Node(4), Node(5)]),
    ...     Node(6, [Node(7, [Node(8), Node(9, [Node(10)])]), Node(11)])
    ... ]))

    print(t)

    >>> list(preorder(t))
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    >>> list(postorder(t))
    [3, 4, 5, 2, 8, 10, 9, 7, 11, 6, 1]
    >>> height(t)
    5
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
