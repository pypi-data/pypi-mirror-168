"""REST System Typings"""

# ISO Starts with Monday as 0 but cameras follow Sunday = 0 for time
from types import MappingProxyType
from typing import Final

from async_reolink.api.typings import WeekDays
from async_reolink.api.system.typings import StorageTypes

_INT_WEEKDAY_MAP: Final = MappingProxyType(
    {(int(_e.value) + 1) % 7: _e for _e in WeekDays}
)
_WEEKDAY_INT_MAP: Final = MappingProxyType(
    {_v: _k for (_k, _v) in _INT_WEEKDAY_MAP.items()}
)

_INT_STORAGETYPE_MAP: Final = MappingProxyType(
    {1: StorageTypes.HDD, 2: StorageTypes.SDC}
)
_STORAGETYPE_INT_MAP: Final = MappingProxyType(
    {_v: _k for (_k, _v) in _INT_STORAGETYPE_MAP.items()}
)
