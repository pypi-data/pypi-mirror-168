"""AI Typings"""

from types import MappingProxyType
from typing import Final
from async_reolink.api.ai.typings import AITypes

STR_AITYPES_MAP: Final = MappingProxyType(
    {"dog_cat" if _e == AITypes.PET else _e.name.lower(): _e for _e in AITypes}
)
AITYPES_STR_MAP: Final = MappingProxyType(
    {_v: _k for _k, _v in STR_AITYPES_MAP.items()}
)
