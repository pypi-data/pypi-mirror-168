"""Rest Typings"""

from types import MappingProxyType
from typing import Callable, Final, Protocol, TypeVar, overload
from typing_extensions import Self

from async_reolink.api.typings import StreamTypes

STR_STREAMTYPES_MAP: Final = MappingProxyType(
    {_e.name.lower(): _e for _e in StreamTypes}
)

STREAMTYPES_STR_MAP: Final = MappingProxyType(
    {_v: _k for _k, _v in STR_STREAMTYPES_MAP.items()}
)

_T = TypeVar("_T")


class FactoryValue(Protocol[_T]):
    """Value factory protocol"""

    def __call__(self, create=False) -> _T:
        ...


_VT = TypeVar("_VT")


class Property(Protocol[_T, _VT]):
    """Property Protocol"""

    fget: Callable[[_T], _VT]
    fset: Callable[[_T, _VT], None] | None
    fdel: Callable[[_T], None]

    @overload
    def __get__(self, obj: None, cls: type) -> Self:
        ...

    @overload
    def _get__(self, obj: _T, cls: type) -> _VT:
        ...

    def __get__(self, obj, cls) -> _T:
        ...

    def __set__(self, obj, value) -> None:
        ...
