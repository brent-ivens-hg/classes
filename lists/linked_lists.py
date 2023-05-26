"""
https://www.geeksforgeeks.org/data-structures/linked-list/
"""
from collections.abc import Sequence


class Node:
    def __init__(self, __data: ..., __next: 'Node' = None, /):
        self.data = __data
        self.next = __next

    def __repr__(self):
        return f'{self.__class__.__name__}{self.data, self.next}'

    def __next__(self):
        return self.next


class LinkedList:
    def __init__(self, seq: Sequence | None = None):
        if seq is None:
            self.head = self.tail = None
        elif isinstance(seq, Sequence):
            self.head = self.tail = Node(seq[0])
            for x in seq[1:]:
                self.tail.next = Node(x)
                self.tail = self.tail.next
        else:
            raise TypeError(f'invalid type {type(seq)}')

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self.head) * bool(self.head)})'

    def __str__(self):
        stringify = lambda node: str(node.data) if node.next is None else f'{node.data} -> {stringify(node.next)}'
        return f'[{stringify(self.head) if self.head else ""}]'

    def __getitem__(self, item):
        if not isinstance(item, int): raise TypeError(f'invalid type {type(item)}')
        try:
            if item == 0:
                if self.head is None: raise AttributeError
                return self.head
            if item > 0:
                a = self.head
                for _ in range(item):
                    a = a.next
                return a
            if item < 0:
                item = -item
                a = b = self.head
                for _ in range(item - 1):
                    b = b.next
                while b.next: a, b = a.next, b.next
                return a
        except AttributeError:
            raise IndexError(f'{self.__class__.__name__} index out of range') from None

    def insert(self):
        """
        def insort(self, data):
            def _insort(head, data):
                if head and head.data < data:
                    head.next = _insort(head.next, data)
                    return head
                n = Node(data)
                n.next = head
                return n

            self.head = _insort(self.head, data)
        """

    def append(self, data):
        """
        def append(a, b):
            if a and b:
                c = deepcopy(a)
                tail = c
                while tail.next:
                    tail = tail.next
                tail.next = b
                return c
            return a or b
        """
        pass

    def extend(self, *data):
        pass

    def prepend(self, data):
        pass

    def extend_left(self, *data):
        pass

    def concat(self, other):
        pass


lst = LinkedList([1, 2, 4, 5])
print(lst)
print(lst.head.data)
print(lst.tail.data)

for x in lst: print(x)

'''
lst = LinkedList('ABCD')
print(lst)
print(lst[1])

lst = LinkedList()
print(lst)
print(LinkedList([1]))
print(LinkedList([1, 2]))
'''
