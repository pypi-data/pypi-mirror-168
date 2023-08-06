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
