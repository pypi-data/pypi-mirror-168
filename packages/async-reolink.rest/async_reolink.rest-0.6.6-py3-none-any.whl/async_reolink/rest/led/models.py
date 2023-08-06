"""LED Models"""

from typing import Callable, Final
from async_reolink.api.led import typings
from async_reolink.api.typings import SimpleTimeValue

from ..typings import FactoryValue

from ..ai.models import AITypesMap, MutableAITypesMap

# pylint: disable=missing-function-docstring


class LightingSchedule(typings.LightingSchedule):
    """Lighting Schedule"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        super().__init__()
        self._factory = factory

    class StartTime(SimpleTimeValue):
        """Start Time"""

        _HOUR_KEY: Final = "StartHour"
        _MIN_KEY: Final = "StartMin"

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        @property
        def hour(self):
            if (value := self._factory()) is None:
                return 0
            return value.get(type(self)._HOUR_KEY, 0)

        @property
        def minute(self):
            if (value := self._factory()) is None:
                return 0
            return value.get(type(self)._MIN_KEY, 0)

    @property
    def start(self):
        return type(self).StartTime(self._factory)

    class EndTime(SimpleTimeValue):
        """End Time"""

        __slots__ = ("_factory",)

        _HOUR_KEY: Final = "EndHour"
        _MIN_KEY: Final = "EndMin"

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        @property
        def hour(self):
            if (value := self._factory()) is None:
                return 0
            return value.get(type(self)._HOUR_KEY, 0)

        @property
        def minute(self):
            if (value := self._factory()) is None:
                return 0
            return value.get(type(self)._MIN_KEY, 0)

    @property
    def end(self):
        return type(self).EndTime(self._factory)


class MutableLightingSchedule(LightingSchedule):
    """Mutable Lighting schedule"""

    def __init__(self, factory: FactoryValue[dict]) -> None:
        super().__init__(factory)
        self._factory = factory

    class StartTime(LightingSchedule.StartTime):
        """Start Time"""

        def __init__(self, factory: FactoryValue[dict]) -> None:
            super().__init__(factory)
            self._factory = factory

        @LightingSchedule.StartTime.hour.setter
        def hour(self, value):
            if (value := self._factory(True)) is not None:
                value[type(self)._HOUR_KEY] = value

        @LightingSchedule.StartTime.minute.setter
        def minute(self, value):
            if (value := self._factory(True)) is not None:
                value[type(self)._MIN_KEY] = value

    def _update_time(self, _time: SimpleTimeValue, value: SimpleTimeValue):
        _time.hour = value.hour
        _time.minute = value.minute

    @LightingSchedule.start.setter
    def start(self, value):
        self._update_time(self.start, value)

    class EndTime(LightingSchedule.EndTime):
        """End Time"""

        def __init__(self, factory: FactoryValue[dict]) -> None:
            super().__init__(factory)
            self._factory = factory

        @LightingSchedule.EndTime.hour.setter
        def hour(self, value):
            if (value := self._factory(True)) is not None:
                value[type(self)._HOUR_KEY] = value

        @LightingSchedule.EndTime.minute.setter
        def minute(self, value):
            if (value := self._factory(True)) is not None:
                value[type(self)._MIN_KEY] = value

    @LightingSchedule.end.setter
    def end(self, value: SimpleTimeValue):
        self._update_time(self.end, value)


class WhiteLedInfo(typings.WhiteLedInfo):
    """White Led Info"""

    _BRIGHT_KEY: Final = "bright"
    _AUTO_KEY: Final = "auto"
    _MODE_KEY: Final = "mode"
    _STATE_KEY: Final = "state"
    _SCHED_KEY: Final = "LightingSchedule"
    _AI_KEY: Final = "wlAiDetectType"

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        super().__init__()
        self._factory = factory

    @property
    def brightness(self):
        if (value := self._factory()) is None:
            return 100
        return value.get(type(self)._BRIGHT_KEY, 100)

    @property
    def auto_mode(self):
        if (value := self._factory()) is None:
            return 0
        return value.get(type(self)._AUTO_KEY, 0)

    @property
    def brightness_state(self):
        if (value := self._factory()) is None:
            return 0
        return value.get(type(self)._MODE_KEY, 0)

    @property
    def state(self):
        if (value := self._factory()) is None:
            return 0
        return value.get(type(self)._STATE_KEY, 0)

    def _get_sched(self) -> dict:
        if (value := self._factory()) is None:
            return None
        return value.get(type(self)._SCHED_KEY, None)

    @property
    def lighting_schedule(self):
        return LightingSchedule(self._get_sched)

    def _get_ai(self) -> dict:
        if (value := self._factory()) is None:
            return None
        return value.get(type(self)._AI_KEY, None)

    @property
    def ai_detection_type(self):
        return AITypesMap(self._get_ai)


class MutableWhiteLedInfo(WhiteLedInfo):
    """White Led Info"""

    def __init__(self, factory: FactoryValue[dict]) -> None:
        super().__init__(factory)
        self._factory = factory

    @WhiteLedInfo.brightness.setter
    def brightness(self, value):
        if (value := self._factory(True)) is not None:
            value[type(self)._BRIGHT_KEY] = value

    @WhiteLedInfo.auto_mode.setter
    def auto_mode(self, value):
        if (value := self._factory(True)) is not None:
            value[type(self)._AUTO_KEY] = value

    @WhiteLedInfo.brightness_state.setter
    def brightness_state(self, value):
        if (value := self._factory(True)) is not None:
            value[type(self)._MODE_KEY] = value

    @WhiteLedInfo.state.setter
    def state(self, value):
        if (value := self._factory(True)) is not None:
            value[type(self)._STATE_KEY] = value

    def _get_sched(self, create=False) -> dict:
        if not create:
            return super()._get_sched()
        if (value := self._factory(True)) is None:
            return None
        return value.setdefault(type(self)._SCHED_KEY, {})

    @WhiteLedInfo.lighting_schedule.getter
    def lighting_schedule(self):
        return MutableLightingSchedule(self._get_sched)

    @lighting_schedule.setter
    def lighting_schedule(self, value: typings.LightingSchedule):
        _sched = self.lighting_schedule
        _sched.start = value.start
        _sched.end = value.end

    def _get_ai(self, create=False) -> dict:
        if not create:
            return super()._get_ai()
        if (value := self._factory(True)) is None:
            return None
        return value.setdefault(type(self)._AI_KEY, {})

    @WhiteLedInfo.ai_detection_type.getter
    def ai_detection_type(self):
        return MutableAITypesMap(self._get_ai)

    @ai_detection_type.setter
    def ai_detection_type(self, value):
        _type: MutableAITypesMap = self.ai_detection_type
        _type.update(value)
