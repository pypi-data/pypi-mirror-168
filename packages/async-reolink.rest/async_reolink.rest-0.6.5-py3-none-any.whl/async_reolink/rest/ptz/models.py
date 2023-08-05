"""REST PTZ Models"""

from typing import Callable, Final, Iterable, MutableSequence, Sequence, overload
from async_reolink.api.ptz import typings

from ..typings import FactoryValue

from ..commands import _CHANNEL_KEY

# pylint: disable=missing-function-docstring

_ID_KEY: Final = "id"
_ENABLE_KEY: Final = "enable"
_NAME_KEY: Final = "name"

_FOCUS_KEY: Final = "focus"
_ZOOM_KEY: Final = "zoom"


class ZoomFocus(typings.ZoomFocus):
    """REST PTZ Zoom/Focus"""

    __slots__ = ("_value",)

    def __init__(self, value: dict) -> None:
        super().__init__()
        if value is None:
            value = {}
        self._value = value

    def _get_pos(self, key: str):
        if (value := self._value.get(key, None)) is None:
            return 0
        return value.get("pos", 0)

    @property
    def zoom(self) -> int:
        return self._get_pos(_ZOOM_KEY)

    @property
    def focus(self) -> int:
        return self._get_pos(_FOCUS_KEY)


class Preset(typings.Preset):
    """REST PTZ Preset"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    @property
    def channel_id(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get(_CHANNEL_KEY, 0)

    @property
    def id(self) -> int:  # pylint: disable=invalid-name
        if (value := self._factory()) is None:
            return 0
        return value.get(_ID_KEY, 0)

    @property
    def enabled(self) -> bool:
        if (value := self._factory()) is None:
            return 0
        return value.get(_ENABLE_KEY, 0)

    @property
    def name(self) -> str:
        if (value := self._factory()) is None:
            return ""
        return value.get(_NAME_KEY, "")


class MutablePreset(Preset):
    """Mutable PTZ Preset"""

    __slots__ = ()

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, value: typings.Preset) -> None:
        ...

    @overload
    def __init__(self, factory: FactoryValue[dict]) -> None:
        ...

    def __init__(self, factory: FactoryValue[dict] = None) -> None:
        source: typings.Preset = None
        if not callable(factory):
            value = factory
            if not isinstance(value, dict):
                source = value
                value = {}

            def _factory(*_):
                return value

            factory = _factory
        super().__init__(factory)
        self._factory = factory
        if source is not None:
            self.channel_id = source.channel_id
            self.enabled = source.enabled
            self.id = source.id
            self.name = source.name

    @Preset.channel_id.setter
    def channel_id(self, value):
        if (value := self._factory(True)) is not None:
            value[_CHANNEL_KEY] = value

    @Preset.id.setter
    def id(self, value):
        if (value := self._factory(True)) is not None:
            value[_ID_KEY] = value

    @Preset.name.setter
    def name(self, value):
        if (value := self._factory(True)) is not None:
            value[_NAME_KEY] = value


_DWELL_TIME_KEY: Final = "dwellTime"
_SPEED_KEY: Final = "speed"


class PatrolPreset(typings.PatrolPreset):
    """REST PTZ Patrol Preset"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    @property
    def dwell_time(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get(_DWELL_TIME_KEY, 0)

    @property
    def preset_id(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get(_ID_KEY, 0)

    @property
    def speed(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get(_SPEED_KEY, 0)


class MutablePatrolPreset(PatrolPreset):
    """REST Mutable PTZ Patrol Preset"""

    __slots__ = ()

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, value: typings.PatrolPreset) -> None:
        ...

    @overload
    def __init__(self, factory: FactoryValue[dict]) -> None:
        ...

    def __init__(
        self,
        factory: FactoryValue[dict] = None,
    ) -> None:
        source: typings.Preset = None
        if not callable(factory):
            value = factory
            if not isinstance(value, dict):
                source = value
                value = {}

            def _factory(*_):
                return value

            factory = _factory
        super().__init__(factory)
        self._factory = factory
        if source is not None:
            self.dwell_time = source.dwell_time
            self.preset_id = source.preset_id
            self.speed = source.speed

    @PatrolPreset.dwell_time.setter
    def dwell_time(self, value):
        if (value := self._factory(True)) is not None:
            value[_DWELL_TIME_KEY] = value

    preset_id = Preset.id

    @PatrolPreset.speed.setter
    def speed(self, value):
        if (value := self._factory(True)) is not None:
            value[_SPEED_KEY] = value


class _PatrolPresets(Sequence[PatrolPreset]):
    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], list]) -> None:
        self._factory = factory

    def __getitem__(self, __k: int):
        def _factory():
            if (value := self._factory()) is None:
                return None
            return value[__k]

        return PatrolPreset(_factory)

    def __len__(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return len(value)


class _MutablePatrolPresets(MutableSequence[MutablePatrolPreset]):
    __slots__ = ("_factory",)

    def __init__(self, factory: FactoryValue[list]) -> None:
        self._factory = factory

    def __getitem__(self, __k: int):
        def _factory():
            if (value := self._factory()) is None:
                return None
            return value[__k]

        return MutablePatrolPreset(_factory)

    def __setitem__(self, __k: int, __v: MutablePatrolPreset):
        if (value := self._factory(True)) is not None:
            value[__k] = __v._factory(True)

    def __delitem__(self, __k: int):
        if (value := self._factory()) is not None:
            del value[__k]

    def _insert(self, index: int, value: dict):
        if (_value := self._factory(True)) is not None:
            _value.insert(index, value)

    def append(self, value: typings.PatrolPreset) -> None:
        return super().append(value)

    def insert(self, index: int, value: typings.PatrolPreset):
        if not isinstance(value, MutablePatrolPreset):
            value = MutablePatrolPreset(value)
        # pylint: disable=protected-access
        self._insert(index, value._factory(True))

    def clear(self) -> None:
        if (value := self._factory()) is not None:
            value.clear()

    def __len__(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return len(value)


_PRESET_KEY: Final = "preset"
_RUNNING_KEY: Final = "running"


class Patrol(typings.Patrol):
    """REST PTZ Patrol"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    channel_id = Preset.channel_id
    id = Preset.id
    enabled = Preset.enabled
    name = Preset.name

    def _get_presets(self) -> list:
        if (value := self._factory()) is None:
            return None
        return value.get(_PRESET_KEY, None)

    @property
    def presets(self):
        return _PatrolPresets(self._get_presets)

    @property
    def running(self) -> bool:
        if (value := self._factory()) is None:
            return 0
        return value.get(_RUNNING_KEY, 0)


class MutablePatrol(Patrol):
    """Mutable REST PTZ Patrol"""

    __slots__ = ()

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, value: typings.Patrol) -> None:
        ...

    @overload
    def __init__(self, factory: FactoryValue[dict]) -> None:
        ...

    def __init__(self, factory: FactoryValue[dict] = None) -> None:
        source: typings.Patrol = None
        if not callable(factory):
            value = factory
            if not isinstance(value, dict):
                source = value
                value = {}

            def _factory(*_):
                return value

            factory = _factory
        super().__init__(factory)
        self._factory = factory
        if source is not None:
            self.channel_id = source.channel_id
            self.enabled = source.enabled
            self.id = source.id
            self.name = source.name
            self.presets = source.presets

    channel_id = MutablePreset.channel_id
    id = MutablePreset.id
    enabled = MutablePreset.enabled
    name = MutablePreset.name

    def _get_presets(self, create=False) -> list:
        _key: Final = _PRESET_KEY
        if (value := self._factory(create)) is None:
            return None
        if _key in value or not create:
            return value.get(_key, None)
        return value.setdefault(_key, {})

    @property
    def presets(self):
        return _MutablePatrolPresets(self._get_presets)

    @presets.setter
    def presets(self, value: Iterable[typings.PatrolPreset]):
        _presets = self.presets
        _presets.clear()
        for preset in value:
            _presets.append(preset)


class Track(typings.Track):
    """REST Track (Tattern)"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    id = Preset.id
    enabled = Preset.enabled
    name = Preset.name
    running = Patrol.running


class MutableTrack(Track):
    """Mutable REST Track (Tattern)"""

    __slots__ = ()

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, value: typings.Track) -> None:
        ...

    @overload
    def __init__(self, factory: FactoryValue[dict]) -> None:
        ...

    def __init__(self, factory: FactoryValue[dict] = None) -> None:
        source: typings.Track = None
        if not callable(factory):
            value = factory
            if not isinstance(value, dict):
                source = value
                value = {}

            def _factory(*_):
                return value

            factory = _factory
        super().__init__(factory)
        self._factory = factory
        if source is not None:
            self.enabled = source.enabled
            self.id = source.id
            self.name = source.name
            self.running = source.running

    id = MutablePreset.id
    enabled = MutablePreset.enabled
    name = MutablePreset.name
    running = MutablePatrol.running
