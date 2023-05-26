"""
Binary Trees
"""
from collections.abc import Generator, Callable, Iterable
from typing import Generic, TypeVar

_T = TypeVar('_T')


class Node(Generic[_T]):
    def __init__(self, value: _T, left: 'Node[_T] | None' = None, right: 'Node[_T] | None' = None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}{self.value, self.left, self.right}'


def pprint(node: Node[_T] | None, space: int = 0, level_space: int = 5, property_: str = 'value') -> None:
    if node is None: return
    space += level_space
    pprint(node.right, space, level_space, property_)
    # print() # neighbor space
    for i in range(level_space, space): print(end=' ')
    print(f'|{getattr(node, property_)}|<')
    pprint(node.left, space, level_space, property_)


# pprint(Node(1, Node(2,
#                     Node(4, Node(8, Node(16), Node(17)), Node(9, Node(18), Node(19))),
#                     Node(5, Node(10, Node(20), Node(21)), Node(11, Node(22), Node(23)))),
#
#             Node(3,
#                  Node(6, Node(12, Node(24), Node(25)), Node(13, Node(26), Node(27))),
#                  Node(7, Node(14, Node(28), Node(29)), Node(15, Node(30), Node(31))))), level_space=10)


def as_list(node: Node[_T]) -> list[_T] | None:
    if node is None: return None
    return [node.value, as_list(node.left), as_list(node.right)]


def create_tree(seed: _T,
                op_left: Callable[[_T], _T],
                op_right: Callable[[_T], _T],
                base_case: Callable[[_T], bool],
                left_case: Callable[[_T], bool] = lambda value: True,
                right_case: Callable[[_T], bool] = lambda value: True) -> Node | None:
    """
    >>> create_tree(
    ...     seed=12,
    ...     op_left=lambda n: n // 2,
    ...     op_right=lambda n: n - 1,
    ...     base_case=lambda n: n <= 0,
    ...     left_case=lambda n: n % 2 == 0
    ...     # right_case == base_case
    ... )
    Node(12, Node(6, Node(3, None, Node(2, Node(1, None, None), Node(1, None, None))), Node(5, None, Node(4, Node(2, Node(1, None, None), Node(1, None, None)), Node(3, None, Node(2, Node(1, None, None), Node(1, None, None)))))), Node(11, None, Node(10, Node(5, None, Node(4, Node(2, Node(1, None, None), Node(1, None, None)), Node(3, None, Node(2, Node(1, None, None), Node(1, None, None))))), Node(9, None, Node(8, Node(4, Node(2, Node(1, None, None), Node(1, None, None)), Node(3, None, Node(2, Node(1, None, None), Node(1, None, None)))), Node(7, None, Node(6, Node(3, None, Node(2, Node(1, None, None), Node(1, None, None))), Node(5, None, Node(4, Node(2, Node(1, None, None), Node(1, None, None)), Node(3, None, Node(2, Node(1, None, None), Node(1, None, None))))))))))))
    """
    if base_case(seed): return None
    res = Node(seed)
    if left_case(seed):  res.left = create_tree(op_left(seed), op_left, op_right, base_case, left_case, right_case)
    if right_case(seed): res.right = create_tree(op_right(seed), op_left, op_right, base_case, left_case, right_case)
    return res


def depth(node: Node[_T] | None) -> int:
    if node is None: return 0
    return 1 + max(depth(node.left), depth(node.right))


def equals(a: Node[_T] | None, b: Node[_T] | None) -> bool:
    if not (isinstance(a, Node) and isinstance(b, Node)):
        return a == b
    return a.value == b.value and equals(a.left, b.left) and equals(a.right, b.right)


def values(nodes: Iterable[Node[_T]]) -> list[_T]:
    return [node.value for node in nodes]


# DEPTH FIRST ORDER(S) #


def inorder(node: Node[_T]) -> Generator[Node[_T], None, None]:
    """
    >>> values(inorder(Node(1, Node(2, Node(4), Node(5, Node(7), Node(8))), Node(3, right=Node(6, Node(9))))))
    [4, 2, 7, 5, 8, 1, 3, 9, 6]
    """
    if node is None: return
    yield from inorder(node.left)
    yield node
    yield from inorder(node.right)


def preorder(node: Node[_T]) -> Generator[Node[_T], None, None]:
    """
    >>> values(preorder(Node(1, Node(2, Node(4), Node(5, Node(7), Node(8))), Node(3, right=Node(6, Node(9))))))
    [1, 2, 4, 5, 7, 8, 3, 6, 9]
    """
    if node is None: return
    yield node
    yield from preorder(node.left)
    yield from preorder(node.right)


def postorder(node: Node[_T]) -> Generator[Node[_T], None, None]:
    """
    >>> values(postorder(Node(1, Node(2, Node(4), Node(5, Node(7), Node(8))), Node(3, right=Node(6, Node(9))))))
    [4, 7, 8, 5, 2, 9, 6, 3, 1]
    """
    if node is None: return
    yield from postorder(node.left)
    yield from postorder(node.right)
    yield node


def from_inorder_and_preorder(inorder_sequence: list[_T],
                              preorder_sequence: list[_T]) -> Node[_T] | None:
    """
    >>> equals(from_inorder_and_preorder([9, 3, 1, 0, 4, 2, 7, 6, 8, 5], [2, 3, 9, 0, 1, 4, 8, 7, 6, 5]),
    ...        Node(2, Node(3, Node(9), Node(0, Node(1), Node(4))), Node(8, Node(7, right=Node(6)), Node(5))))
    True
    """
    if not preorder_sequence: return None
    root = Node(preorder_sequence[0])
    idx = inorder_sequence.index(root.value)
    root.left = from_inorder_and_preorder(inorder_sequence[:idx],
                                          preorder_sequence[1:idx + 1])  # indices -> exclude root (first)
    root.right = from_inorder_and_preorder(inorder_sequence[idx + 1:],
                                           preorder_sequence[idx + 1:])  # indices ->  exclude root (first)
    return root


def from_inorder_and_postorder(inorder_sequence: list[_T],
                               postorder_sequence: list[_T]) -> Node[_T] | None:
    """
    >>> equals(from_inorder_and_postorder([9, 3, 1, 0, 4, 2, 7, 6, 8, 5], [9, 1, 4, 0, 3, 6, 7, 5, 8, 2]),
    ...        Node(2, Node(3, Node(9), Node(0, Node(1), Node(4))), Node(8, Node(7, right=Node(6)), Node(5))))
    True
    """
    if not postorder_sequence: return None
    root = Node(postorder_sequence[-1])
    idx = inorder_sequence.index(root.value)
    root.left = from_inorder_and_postorder(inorder_sequence[:idx],
                                           postorder_sequence[:idx])
    root.right = from_inorder_and_postorder(inorder_sequence[idx + 1:],
                                            postorder_sequence[idx:-1])  # indices -> exclude root (last)
    return root


# BREADTH FIRST ORDER #

def levels(node: Node[_T]) -> Generator[list[Node[_T]], None, None]:
    level = [node]
    while level:
        yield level
        level = [child for node in level for child in (node.left, node.right) if child is not None]


def level_order(node: Node[_T]) -> Generator[Node[_T], None, None]:
    yield node
    for child in level_order(node):
        if child.left is None and child.right is None:
            return  # Stop The Recursion As Soon As We Hit A Leaf
        yield from filter(None, (child.left, child.right))


def paths(node: Node, path: list[Node]) -> Generator[list[Node], None, None]:
    if node is None:
        return
    if node.left is None and node.right is None:
        yield path + [node]
        return
    yield from paths(node.left, path + [node])
    yield from paths(node.right, path + [node])


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    # level_order_and_postorder ?
    # generate_random_tree(number_of_nodes)
    # pprint(from_inorder_and_postorder([9, 3, 1, 0, 4, 2, 7, 6, 8, 5], [9, 1, 4, 0, 3, 6, 7, 5, 8, 2]))
    # tree = Node(8,
    #             Node(3, Node(1), Node(6, Node(4), Node(7))),
    #             Node(10, right=Node(14, Node(13)))
    #             )
    # pprint(tree)
    # print(list(values(inorder(tree))))

    t = Node(1, Node(2, Node(4), Node(5, Node(7), Node(8))), Node(3, right=Node(6, Node(9))))
    print(values(postorder(t)))
    print([4, 7, 8, 5, 2, 9, 6, 3, 1])
