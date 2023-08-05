"""REST Network Typings"""

from types import MappingProxyType
from typing import Final

from async_reolink.api.network.typings import LinkTypes

STR_LINKTYPES_MAP: Final = MappingProxyType(
    {"Static" if _e == LinkTypes.STATIC else _e.name.upper(): _e for _e in LinkTypes}
)

LINKTYPES_STR_MAP: Final = MappingProxyType(
    {_v: _k for _k, _v in STR_LINKTYPES_MAP.items()}
)
