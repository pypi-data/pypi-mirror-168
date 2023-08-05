"""Seeding Helper"""

import random
import string


_rnd = random.SystemRandom()
_RND_SET = string.printable


class Seed:
    """Simple Random String Generator"""

    def __init__(self, _min: int = 16, _max: int = 16) -> None:
        self._min = _min
        self._max = _max

    @property
    def value(self):
        """Get Random Seed Value"""
        return str(self)

    def __str__(self) -> str:
        rng = _rnd.randint(self._min, self._max)
        return "".join(_rnd.choice(_RND_SET) for _ in range(rng))
