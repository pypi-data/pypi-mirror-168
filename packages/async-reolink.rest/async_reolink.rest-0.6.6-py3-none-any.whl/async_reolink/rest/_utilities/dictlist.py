"""List as a Dictionary"""

from typing import Callable, Generator, Mapping, TypeVar, overload


_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class DictList(Mapping[_KT, _VT]):
    """list as a Dictionary"""

    __slots__ = ("_key", "_value", "_type")

    @overload
    def __init__(
        self: "DictList[int,_VT]",
        key: str,
        value: list,
        __type: Callable[[Callable[[], dict]], _VT],
    ) -> None:
        ...

    def __init__(
        self,
        key: str,
        value: list,
        __type: Callable[[Callable[[], dict]], _VT],
    ) -> None:
        self._key = key
        self._value = value
        self._type = __type

    def _factory(self):
        return self._value

    def _get_item(self, __k: _KT) -> dict:
        return (
            next(
                (
                    _d
                    for _d in value
                    if isinstance(_d, dict) and _d.get(self._key, None) == __k
                ),
                None,
            )
            if (value := self._factory()) is not None
            else None
        )

    def __getitem__(self, __k: _KT):
        def _factory():
            return self._get_item(__k)

        return self._type(_factory)

    def __iter__(self) -> Generator[int, None, None]:
        if (value := self._factory()) is None:
            return
        for _d in value:
            if isinstance(_d, dict) and (__k := _d.get(self._key, None)) is not None:
                yield __k

    def __contains__(self, __o: _KT):
        return self._get_item(__o) is not None

    def __len__(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return len(value)
