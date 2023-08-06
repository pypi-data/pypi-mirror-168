"""REST LED Typings"""

from types import MappingProxyType
from typing import Final
from async_reolink.api.led.typings import LightStates

STR_LIGHTSTATES_MAP: Final = MappingProxyType(
    {"Auto": LightStates.AUTO, "On": LightStates.ON, "Off": LightStates.OFF}
)

LIGHTSTATES_STR_MAP: Final = MappingProxyType(
    {_v: _k for _k, _v in STR_LIGHTSTATES_MAP.items()}
)
