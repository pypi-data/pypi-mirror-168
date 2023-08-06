"""REST PTZ Commands"""

from typing import (
    TYPE_CHECKING,
    Callable,
    Final,
    Iterable,
    MutableSequence,
    cast,
)
from async_reolink.api.commands import ptz
from async_reolink.api.ptz import typings

from .._utilities.dictlist import DictList

from ..models import MinMaxRange, StringRange

from ..ptz.typings import (
    OPERATION_STR_MAP,
    STR_OPERATION_MAP,
    STR_ZOOMOPERATION_MAP,
    ZOOMOPERATION_STR_MAP,
)

from ..ptz.models import (
    MutablePreset,
    Preset,
    _ID_KEY,
    MutablePatrol,
    Patrol,
    MutableTrack,
    Track,
    ZoomFocus,
)

from ..typings import FactoryValue

from . import (
    _CHANNEL_KEY,
    CommandRequest,
    CommandRequestWithChannel,
    CommandResponse,
    CommandResponseTypes,
)

# pylint:disable=missing-function-docstring


class GetPresetRequest(CommandRequestWithChannel, ptz.GetPresetRequest):
    """REST Get Presets Request"""

    __slots__ = ()

    COMMAND: Final = "GetPtzPreset"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


_PRESET_KEY: Final = "PtzPreset"


class _PresetRange:
    __slots__ = ("_value",)

    def __init__(self, value: dict) -> None:
        self._value = value

    def _factory(self):
        return self._value

    def _keyed_factory(self, key: str):
        def _factory() -> dict:
            return (
                value.get(key, None) if (value := self._factory()) is not None else None
            )

        return _factory

    @property
    def id(self):
        return MinMaxRange("", self._keyed_factory("id"))

    @property
    def name(self):
        return StringRange(self._keyed_factory("name"))


class GetPresetResponse(CommandResponse, ptz.GetPresetResponse, test="is_response"):
    """Get Presets Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetPresetRequest.COMMAND)

    def _get_sub_value(self, factory: Callable[[], dict]) -> list:
        return (
            value.get(_PRESET_KEY, None) if (value := factory()) is not None else None
        )

    @property
    def channel_id(self) -> int:
        if (_list := self._get_sub_value(self._get_value)) is None:
            return None
        if (value := next(iter(_list), None)) is None:
            return None
        if TYPE_CHECKING:
            value = cast(dict, value)
        return value.get(_CHANNEL_KEY, None)

    @property
    def presets(self):
        return DictList(_ID_KEY, self._get_sub_value(self._get_value), Preset)

    @property
    def initial_presets(self):
        return DictList(_ID_KEY, self._get_sub_value(self._get_initial), Preset)

    @property
    def presets_range(self):
        if (value := self._get_range()) is not None:
            value = value.get(_PRESET_KEY)
        return _PresetRange(value)


class SetPresetRequest(CommandRequest, ptz.SetPresetRequest):
    """Set Preset Request"""

    __slots__ = ()

    COMMAND: Final = "SetPtzPreset"

    def __init__(
        self,
        preset: typings.Preset = None,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id
        if preset is not None:
            self.preset = preset

    def _get_sub_value(self, create=False) -> dict:
        _key: Final = _PRESET_KEY
        if (parameter := self._get_parameter(create)) is None:
            return None
        if _key in parameter or not create:
            return parameter.get(_key, None)
        return parameter.setdefault(_key, {})

    @property
    def _sub_value(self):
        return self._get_sub_value(True)

    @property
    def channel_id(self) -> int:
        if (value := self._get_sub_value()) is None:
            return 0
        return value.get(_CHANNEL_KEY, 0)

    @channel_id.setter
    def channel_id(self, value):
        self._sub_value[_CHANNEL_KEY] = value

    @property
    def preset(self):
        return MutablePreset(self._get_sub_value)

    @preset.setter
    def preset(self, value):
        if not isinstance(value, MutablePreset):
            value = MutablePreset(value)
        # pylint: disable=protected-access
        self._parameter[_PRESET_KEY] = value._factory(True)


_PATROL_KEY: Final = "PtzPatrol"


class GetPatrolRequest(CommandRequestWithChannel, ptz.GetPatrolRequest):
    """Get Patrol"""

    __slots__ = ()

    COMMAND: Final = "GetPtzPatrol"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


class _PatrolPresetRange:
    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    def _keyed_factory(self, key: str):
        def _factory() -> dict:
            return (
                value.get(key, None) if (value := self._factory()) is not None else None
            )

        return _factory

    @property
    def id(self):
        return MinMaxRange("", self._keyed_factory("id"))

    @property
    def dwell_time(self):
        return MinMaxRange("", self._keyed_factory("dwellTime"))

    @property
    def speed(self):
        return MinMaxRange("", self._keyed_factory("speed"))


class _PatrolRange:
    __slots__ = ("_value",)

    def __init__(self, value: dict) -> None:
        self._value = value

    def _factory(self):
        return self._value

    def _keyed_factory(self, key: str):
        def _factory() -> dict:
            return (
                value.get(key, None) if (value := self._factory()) is not None else None
            )

        return _factory

    @property
    def id(self):
        return MinMaxRange("", self._keyed_factory("id"))

    @property
    def name(self):
        return StringRange(self._keyed_factory("name"))

    @property
    def preset(self):
        return _PatrolPresetRange(self._keyed_factory("preset"))


class GetPatrolResponse(CommandResponse, ptz.GetPatrolResponse, test="is_response"):
    """Get Patrol Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetPatrolRequest.COMMAND)

    def _get_sub_value(self, factory: Callable[[], dict]) -> list:
        return (
            value.get(_PATROL_KEY, None) if (value := factory()) is not None else None
        )

    channel_id = GetPresetResponse.channel_id

    @property
    def patrols(self):
        return DictList(_ID_KEY, self._get_sub_value(self._get_value), Patrol)

    @property
    def initial_presets(self):
        return DictList(_ID_KEY, self._get_sub_value(self._get_initial), Patrol)

    @property
    def presets_range(self):
        if (value := self._get_range()) is not None:
            value = value.get(_PRESET_KEY)
        return _PatrolRange(value)


class SetPatrolRequest(CommandRequest, ptz.SetPatrolRequest):
    """Set  Patrol"""

    __slots__ = ()

    COMMAND: Final = "SetPtzPatrol"

    def __init__(
        self,
        patrol: typings.Patrol = None,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id
        if patrol is not None:
            self.patrol = patrol

    def _get_sub_value(self, create=False) -> dict:
        _key: Final = _PATROL_KEY
        if (parameter := self._get_parameter(create)) is None:
            return None
        if _key in parameter or not create:
            return parameter.get(_key, None)
        return parameter.setdefault(_key, {})

    _sub_value = SetPresetRequest._sub_value

    channel_id = SetPresetRequest.channel_id

    @property
    def patrol(self):
        return MutablePatrol(self._get_sub_value)

    @patrol.setter
    def patrol(self, value):
        if not isinstance(value, MutablePatrol):
            value = MutablePatrol(value)
        # pylint: disable=protected-access
        self._parameter[_PATROL_KEY] = value._factory(True)


_TATTERN_KEY: Final = "PtzTattern"


class GetTatternRequest(CommandRequestWithChannel, ptz.GetTatternRequest):
    """Get Tattern"""

    __slots__ = ()

    COMMAND: Final = "GetPtzTattern"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


class _TrackRange:
    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    def _keyed_factory(self, key: str):
        def _factory() -> dict:
            return (
                value.get(key, None) if (value := self._factory()) is not None else None
            )

        return _factory

    @property
    def id(self):
        return MinMaxRange("", self._keyed_factory("id"))

    @property
    def name(self):
        return StringRange(self._keyed_factory("name"))


class _TracksRange:
    __slots__ = ("_value",)

    def __init__(self, value: dict) -> None:
        self._value = value

    def _factory(self):
        return self._value

    def _keyed_factory(self, key: str):
        def _factory() -> dict:
            return (
                value.get(key, None) if (value := self._factory()) is not None else None
            )

        return _factory

    @property
    def track(self):
        return _TrackRange(self._keyed_factory("track"))


class GetTatternResponse(CommandResponse, ptz.GetTatternResponse):
    """Get Tattern Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetTatternRequest.COMMAND)

    def _get_sub_value(self) -> dict:
        return (
            value.get(_TATTERN_KEY, None)
            if (value := self._get_value()) is not None
            else None
        )

    def _get_tracks(self) -> list:
        if (value := self._get_sub_value()) is None:
            return None
        return value.get("track", None)

    @property
    def channel_id(self) -> int:
        return (
            value.get(_CHANNEL_KEY, 0)
            if (value := self._get_sub_value()) is not None
            else 0
        )

    @property
    def tracks(self):
        return DictList(_ID_KEY, self._get_tracks, Track)

    @property
    def initial_tracks(self):
        return DictList(_ID_KEY, self._get_tracks, Track)

    @property
    def presets_range(self):
        if (value := self._get_range()) is not None:
            value = value.get(_TATTERN_KEY)
        return _TracksRange(value)


class _MutableTracks(MutableSequence[MutableTrack]):
    __slots__ = ("_factory",)

    def __init__(self, factory: FactoryValue[list]) -> None:
        super().__init__()
        self._factory = factory

    def __getitem__(self, __k: int):
        def _factory():
            if (value := self._factory()) is None:
                return None
            return value[__k]

        return MutableTrack(_factory)

    def __setitem__(self, __k: int, __v: MutableTrack):
        if (value := self._factory(True)) is not None:
            value[__k] = __v._factory(True)

    def __delitem__(self, __k: int):
        if (value := self._factory()) is not None:
            del value[__k]

    def _insert(self, index: int, value: dict):
        if (_value := self._factory(True)) is not None:
            _value.insert(index, value)

    def append(self, value: typings.Track) -> None:
        return super().append(value)

    def insert(self, index: int, value: typings.Track):
        if not isinstance(value, MutableTrack):
            value = MutableTrack(value)
        # pylint: disable=protected-access
        self._insert(index, value._factory(True))

    def clear(self) -> None:
        if (value := self._factory()) is not None:
            value.clear()

    def __len__(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return len(value)


class SetTatternRequest(CommandRequest, ptz.SetTatternRequest):
    """Set PTZ Tattern"""

    __slots__ = ()

    COMMAND: Final = "SetPtzTattern"

    def __init__(
        self,
        *tracks: typings.Track,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id
        if len(tracks) > 0:
            _tracks = self.tracks
            for track in tracks:
                _tracks.append(track)

    def _get_sub_value(self, create=False) -> dict:
        _key: Final = _TATTERN_KEY
        if (parameter := self._get_parameter(create)) is None:
            return None
        if _key in parameter or not create:
            return parameter.get(_key, None)
        return parameter.setdefault(_key, {})

    @property
    def _sub_value(self):
        return self._get_sub_value(True)

    @GetTatternRequest.channel_id.setter
    def channel_id(self, value):
        self._sub_value[_CHANNEL_KEY] = value

    def _get_tracks(self, create=False) -> list:
        _key: Final = "track"
        if (value := self._get_sub_value(create)) is None:
            return None
        if _key in value or not create:
            return value.get(_key, None)
        return value.setdefault(_key, [])

    @property
    def tracks(self):
        return _MutableTracks(self._get_tracks)

    @tracks.setter
    def tracks(self, value: Iterable[typings.Track]):
        _tracks = self.tracks
        _tracks.clear()
        for track in value:
            _tracks.append(track)


class GetAutoFocusRequest(CommandRequestWithChannel, ptz.GetAutoFocusRequest):
    """Get PTZ AutoFocus"""

    __slots__ = ()

    COMMAND: Final = "GetAutoFocus"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


_AUTO_FOCUS_KEY: Final = "AutoFocus"
_DISABLE_KEY: Final = "disable"


class GetAutoFocusResponse(
    CommandResponse, ptz.GetAutoFocusResponse, test="is_response"
):
    """Get PTZ AutoFocus Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetAutoFocusRequest.COMMAND)

    def _get_sub_value(self) -> dict:
        return (
            value.get(_AUTO_FOCUS_KEY, None)
            if (value := self._get_value()) is not None
            else None
        )

    channel_id = GetTatternResponse.channel_id

    @property
    def disabled(self) -> bool:
        if (value := self._get_sub_value()) is None:
            return 0
        return value.get(_DISABLE_KEY, 0)


class SetAutoFocusRequest(CommandRequestWithChannel, ptz.SetAutoFocusRequest):
    """Set PTZ AutoFocus"""

    __slots__ = ()

    COMMAND: Final = "AutoFocus"

    def __init__(
        self,
        disabled: bool,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id
        self.disabled = disabled

    def _get_sub_value(self, create=False) -> dict:
        _key: Final = _AUTO_FOCUS_KEY
        if (parameter := self._get_parameter(create)) is None:
            return None
        if _key in parameter or not create:
            return parameter.get(_key, None)
        return parameter.setdefault(_key, {})

    @property
    def _sub_value(self):
        return self._get_sub_value(True)

    channel_id = SetTatternRequest.channel_id

    @GetAutoFocusResponse.disabled.setter
    def disabled(self, value):
        self._sub_value[_DISABLE_KEY] = int(value)


class GetZoomFocusRequest(CommandRequestWithChannel, ptz.GetZoomFocusRequest):
    """Get Zoom and Focus"""

    __slots__ = ()

    COMMAND: Final = "GetZoomFocus"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


_ZOOMFOCUS_KEY: Final = "ZoomFocus"


class _ZoomFocusRange:
    __slots__ = ("_value",)

    def __init__(self, value: dict) -> None:
        self._value = value

    def _factory(self):
        return self._value

    def _keyed_factory(self, key: str):
        def _factory() -> dict:
            return (
                value.get(key, None) if (value := self._factory()) is not None else None
            )

        return _factory

    def __repr__(self):
        return f"<{self.__class__.__name__}: {repr(self._factory())}>"

    def _pos_keyed_factory(self, key: str):
        __factory = self._keyed_factory(key)

        def _factory() -> dict:
            return (
                value.get("pos", None) if (value := __factory()) is not None else None
            )

        return _factory

    @property
    def zoom(self):
        return MinMaxRange("", self._pos_keyed_factory("zoom"))

    @property
    def focus(self):
        return MinMaxRange("", self._pos_keyed_factory("focus"))


class GetZoomFocusResponse(
    CommandResponse, ptz.GetZoomFocusResponse, test="is_response"
):
    """Get Zoom/Focus Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetZoomFocusRequest.COMMAND)

    def _get_sub_value(self, factory: Callable[[], dict] = None):
        if factory is None:
            factory = self._get_value
        return (
            value.get(_ZOOMFOCUS_KEY, None)
            if (value := factory()) is not None
            else None
        )

    channel_id = GetTatternResponse.channel_id

    @property
    def state(self):
        return ZoomFocus(self._get_sub_value())

    @property
    def inital_state(self):
        return ZoomFocus(self._get_sub_value(self._get_initial))

    @property
    def state_range(self):
        return _ZoomFocusRange(self._get_sub_value(self._get_range))


_DEFAULT_ZOOMOPERATION: Final = typings.ZoomOperation.ZOOM
_DEFAULT_ZOOMOPERATION_STR: Final = ZOOMOPERATION_STR_MAP[_DEFAULT_ZOOMOPERATION]


class SetZoomFocusRequest(CommandRequest, ptz.SetZoomFocusRequest):
    """Set Zoom or Focus"""

    __slots__ = ()

    COMMAND: Final = "StartZoomFocus"

    def __init__(
        self,
        operation: typings.ZoomOperation,
        position: int,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id
        self.operation = operation
        self.position = position

    def _get_sub_value(self, create=False) -> dict:
        _key: Final = _ZOOMFOCUS_KEY
        if (parameter := self._get_parameter(create)) is None:
            return None
        if _key in parameter or not create:
            return parameter.get(_key, None)
        return parameter.setdefault(_key, {})

    @property
    def _sub_value(self):
        return self._get_sub_value(True)

    channel_id = SetTatternRequest.channel_id

    @property
    def operation(self) -> typings.ZoomOperation:
        if (value := self._get_sub_value()) is None:
            return _DEFAULT_ZOOMOPERATION
        return STR_ZOOMOPERATION_MAP[value.get("op", _DEFAULT_ZOOMOPERATION_STR)]

    @operation.setter
    def operation(self, value):
        self._sub_value["op"] = ZOOMOPERATION_STR_MAP[value or _DEFAULT_ZOOMOPERATION]

    @property
    def position(self) -> int:
        if (value := self._get_sub_value()) is None:
            return 0
        return value.get("pos", 0)

    @position.setter
    def position(self, value):
        self._sub_value["pos"] = value


_DEFAULT_OPERATION: Final = typings.Operation.AUTO
_DEFAULT_OPERATION_STR: Final = OPERATION_STR_MAP[_DEFAULT_OPERATION]


class SetControlRequest(CommandRequestWithChannel, ptz.SetControlRequest):
    """PTZ Control"""

    __slots__ = ()

    COMMAND: Final = "PtzCtrl"

    def __init__(
        self,
        operation: typings.Operation,
        preset_id: int = None,
        speed: int = None,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id
        self.operation = operation
        self.preset_id = preset_id
        self.speed = speed

    @property
    def operation(self):
        if (value := self._get_parameter()) is None:
            return _DEFAULT_OPERATION
        return STR_OPERATION_MAP[value.get("op", _DEFAULT_OPERATION_STR)]

    @operation.setter
    def operation(self, value):
        self._parameter["op"] = OPERATION_STR_MAP[value or _DEFAULT_OPERATION]

    @property
    def preset_id(self) -> int | None:
        if (value := self._get_parameter()) is None:
            return None
        return value.get("id", None)

    @preset_id.setter
    def preset_id(self, value):
        if value is None:
            if (_value := self._get_parameter()) is not None:
                del _value["id"]
            return
        self._parameter["id"] = value

    @property
    def speed(self) -> int | None:
        if (value := self._get_parameter()) is None:
            return None
        return value.get("speed", None)

    @speed.setter
    def speed(self, value):
        if value is None:
            if (_value := self._get_parameter()) is not None:
                del _value["speed"]
            return
        self._parameter["speed"] = value
