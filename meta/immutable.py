"""
Immutable
"""

__all__ = ['ImmutableMeta']


class ImmutableMeta(type):
    def __setattr__(self, key, value):
        raise AttributeError(f'can\'t set attribute {key!r}')

    def __delattr__(cls, item):
        raise AttributeError(f'can\'t delete attribute {item!r}')
