"""
Radians
"""
from fractions import Fraction
from math import pi


class Radian:
    """
    Ratio/Multiple of Pi
    """

    def __init__(self, num: int, denom: int = 1) -> None:
        if denom == 0: raise ZeroDivisionError(f'Radian({num}, 0)')
        self.__ratio = Fraction(num, denom)

    @property
    def num(self) -> int:
        return self.__ratio.numerator

    @property
    def denom(self) -> int:
        return self.__ratio.denominator

    def __repr__(self) -> str:
        return f'Radian{self.num, self.denom}'

    def __str__(self) -> str:
        if self.num == -1: return f'-pi/{self.denom}'
        if self.num == +1: return f'pi/{self.denom}'
        return f'{self.num}pi/{self.denom}'

    def __pos__(self) -> 'Radian':
        return Radian(+self.num, self.denom)

    def __neg__(self) -> 'Radian':
        return Radian(-self.num, self.denom)

    def __float__(self) -> float:
        return float(self.__ratio) * pi

    def __int__(self) -> int:
        return int(float(self))

    def as_integer_ratio(self) -> tuple[int, int]:
        return self.num, self.denom

    def normalize(self) -> 'Radian':
        """ normalizes to the interval [0, 2(pi)) """
        return Radian(self.num % 2 * self.denom, self.denom)

    def degrees(self) -> float:
        return float(self.__ratio) * 180

    @staticmethod
    def from_degrees(degrees: float) -> 'Radian':
        return Radian(*Fraction(degrees / 180).limit_denominator().as_integer_ratio())


def todo():
    print(float(Radian(2, 5)))
    print(Radian(2, 5).degrees())
    print(Radian.from_degrees(72))
    print(Radian(1, 2), Radian(-3, 2).normalize())
    # print(lambda: Radian(1, 0))
    print(float(Fraction(2, 5)))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
