"""Encoding typings"""

from types import MappingProxyType
from typing import Final

from async_reolink.api.typings import StreamTypes


STR_STREAMTYPES_MAP: Final = MappingProxyType(
    {_e.name.lower() + "Stream": _e for _e in StreamTypes}
)

STREAMTYPES_STR_MAP: Final = MappingProxyType(
    {_v: _k for _k, _v in STR_STREAMTYPES_MAP.items()}
)
