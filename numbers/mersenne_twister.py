"""
Mersenne Twister
"""
from time import time


class MersenneTwister:
    """ Mersenne Twister """

    def __init__(self, seed: int | None = None) -> None:
        # MT19937
        self._W, self._N, self._M, self._R = 32, 624, 397, 31
        self._A = 0x9908B0DF
        self._U, self._D = 11, 0xFFFFFFFF
        self._S, self._B = 7, 0x9D2C5680
        self._T, self._C = 15, 0xEFC60000
        self._L = 18
        self._F = 1812433253
        # create a length n array to store the state of the generator
        self._MT = [0] * self._N
        self._index = self._N + 1
        self._lower_mask = 0xFFFFFFFF
        self._upper_mask = 0x00000000

        self._seed = seed if seed is not None else int(time())
        self._seed_mt()

    @property
    def seed(self) -> int:
        """ :returns: the seed value """
        return self._seed

    @seed.setter
    def seed(self, value: int) -> None:
        """ sets the seed value """
        self._seed = value
        self._seed_mt()

    def _seed_mt(self) -> None:
        """ initializes the generator from a seed """
        self._index = self._N
        self._MT[0] = self._seed
        for i in range(1, self._N):
            self._MT[i] = self._F * (self._MT[i - 1] ^ (self._MT[i - 1] >> (self._W - 2))) + i & self._lower_mask

    def _twist(self) -> None:
        """ generates the next n values from the series x_i """
        for i in range(self._N):
            x = (self._MT[i] & self._upper_mask) + (self._MT[(i + 1) % self._N] & self._lower_mask)
            x_a = x >> 1
            if x & 1: x_a ^= self._A
            self._MT[i] = self._MT[(i + self._M) % self._N] ^ x_a
        self._index = 0

    def _extract_number(self) -> float:
        """ :returns: extracted, tempered value based on MT[index] calling _twist() every n numbers """
        if self._index >= self._N: self._twist()

        y = self._MT[self._index]
        y ^= y >> self._U & self._D
        y ^= y << self._T & self._C
        y ^= y << self._S & self._B
        y ^= y >> self._L

        self._index += 1
        return y & self._lower_mask

    def random(self) -> float:
        """ :returns: uniform distribution in [0,1) """
        return self._extract_number() / 2 ** self._W

    def randint(self, a: int, b: int) -> int:
        """ :returns: random int in [a,b) """
        return int(self.random() / (1 / (b - a)) + a)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
