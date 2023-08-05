"""REST PTZ Typings"""

from types import MappingProxyType
from typing import Final
from async_reolink.api.ptz.typings import ZoomOperation, Operation

STR_OPERATION_MAP: Final = MappingProxyType(
    {
        "Stop": Operation.STOP,
        "Left": Operation.LEFT,
        "Right": Operation.RIGHT,
        "Up": Operation.UP,
        "LeftUp": Operation.LEFT_UP,
        "LeftDown": Operation.LEFT_DOWN,
        "RightUp": Operation.RIGHT_UP,
        "RightDown": Operation.RIGHT_DOWN,
        "IrisDec": Operation.IRIS_SHRINK,
        "IrisInc": Operation.IRIS_ENLARGE,
        "ZoomDec": Operation.ZOOM_OUT,
        "ZoomInc": Operation.ZOOM_IN,
        "FocusInc": Operation.FOCUS_BACK,
        "FocusDec": Operation.FOCUS_FORWARD,
        "Auto": Operation.AUTO,
        "StartPatrol": Operation.PATROL_START,
        "StopPatrol": Operation.PATROL_STOP,
        "ToPos": Operation.TO_PRESET,
    }
)

OPERATION_STR_MAP: Final = MappingProxyType(
    {_v: _k for _k, _v in STR_OPERATION_MAP.items()}
)

STR_ZOOMOPERATION_MAP: Final = MappingProxyType(
    {"ZoomPos": ZoomOperation.ZOOM, "FocusPos": ZoomOperation.FOCUS}
)

ZOOMOPERATION_STR_MAP: Final = MappingProxyType(
    {_v: _k for _k, _v in STR_ZOOMOPERATION_MAP.items()}
)
