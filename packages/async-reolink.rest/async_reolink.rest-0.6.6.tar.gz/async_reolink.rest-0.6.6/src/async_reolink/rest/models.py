"""General Models"""

from typing import Callable, Generic, TypeVar, overload

_T = TypeVar("_T")


class MinMaxRange(Generic[_T]):
    """Min/Max values"""

    __slots__ = ("_suffix", "_factory")

    @overload
    def __init__(self: "MinMaxRange[int]", suffix: str, factory: Callable[[], dict]):
        ...

    def __init__(self, suffix: str, factory: Callable[[], dict]) -> None:
        self._suffix = suffix
        self._factory = factory

    @property
    def min(self) -> _T | None:
        """minimum value"""
        if (value := self._factory()) is None:
            return None
        return value.get("min" + self._suffix, None)

    @property
    def max(self) -> _T | None:
        """maximum value"""
        if (value := self._factory()) is None:
            return None
        return value.get("max" + self._suffix, None)


class StringRange:
    """String Ranges"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    @property
    def length(self):
        """length ranges"""
        return MinMaxRange("Len", self._factory)
