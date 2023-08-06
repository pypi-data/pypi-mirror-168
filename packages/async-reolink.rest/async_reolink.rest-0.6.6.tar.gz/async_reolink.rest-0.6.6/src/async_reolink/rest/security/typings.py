"""REST Securiy typings"""

from types import MappingProxyType
from typing import Final
from async_reolink.api.security import typings

_STR_LEVELTYPE_MAP: Final = MappingProxyType(
    {
        "guest": typings.LevelTypes.GUEST,
        "user": typings.LevelTypes.USER,
        "admin": typings.LevelTypes.ADMIN,
    }
)
_LEVELTYPE_STR_MAP: Final = MappingProxyType(
    {_v: _k for _k, _v in _STR_LEVELTYPE_MAP.items()}
)
