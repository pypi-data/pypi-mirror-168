"""System models"""

from typing import Callable, Final, TypeVar
from async_reolink.api.commands import system
from async_reolink.api.system import typings
from async_reolink.api.typings import WeekDays
from .typings import _INT_WEEKDAY_MAP, _INT_STORAGETYPE_MAP

# pylint: disable=missing-function-docstring
# pylint: disable=too-few-public-methods

_T = TypeVar("_T")


class DeviceInfo(typings.DeviceInfo):
    """Device Info"""

    __slots__ = ("_value",)

    def __init__(self, value: dict) -> None:
        super().__init__()
        if value is None:
            value = {}
        self._value = value

    def _factory(self):
        return self._value

    class IO(typings.DeviceInfo.IO):
        """IO"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        @property
        def inputs(self):
            if (value := self._factory()) is None:
                return 0
            return value.get("IOInputNum", 0)

        @property
        def outputs(self):
            if (value := self._factory()) is None:
                return 0
            return value.get("IOOutputNum", 0)

    @property
    def io(self):
        return type(self).IO(self._factory)

    class Version(typings.DeviceInfo.Version):
        """Versions"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        @property
        def firmware(self):
            if (value := self._factory()) is None:
                return ""
            return value.get("firmVer", "")

        @property
        def framework(self):
            if (value := self._factory()) is None:
                return ""
            return value.get("frameworkVer", "")

        @property
        def hardware(self):
            if (value := self._factory()) is None:
                return ""
            return value.get("hardVer", "")

        @property
        def config(self):
            if (value := self._factory()) is None:
                return ""
            return value.get("cfgVer", "")

    @property
    def version(self):
        return type(self).Version(self._factory)

    @property
    def audio_sources(self):
        if (value := self._factory()) is None:
            return 0
        return value.get("audioNum", 0)

    @property
    def build_day(self):
        if (value := self._factory()) is None:
            return ""
        return value.get("buildDay", "")

    @property
    def channels(self):
        if (value := self._factory()) is None:
            return 0
        return value.get("channelNum", 0)

    @property
    def detail(self):
        if (value := self._factory()) is None:
            return ""
        return value.get("detail", "")

    @property
    def disks(self):
        if (value := self._factory()) is None:
            return 0
        return value.get("diskNum", 0)

    @property
    def model(self):
        if (value := self._factory()) is None:
            return ""
        return value.get("model", "")

    @property
    def name(self):
        if (value := self._factory()) is None:
            return ""
        return value.get("name", "")

    @property
    def type(self):
        if (value := self._factory()) is None:
            return ""
        return value.get("type", "")

    @property
    def wifi(self):
        if (value := self._factory()) is None:
            return False
        return value.get("wifi", False)

    # @property
    def B845(self):
        if (value := self._factory()) is None:
            return 0
        return value.get("", 0)

    @property
    def exact_type(self):
        if (value := self._factory()) is None:
            return ""
        return value.get("exactType", "")

    @property
    def serial(self):
        if (value := self._factory()) is None:
            return ""
        return value.get("serial", "")

    @property
    def pak_suffix(self):
        if (value := self._factory()) is None:
            return ""
        return value.get("pakSuffix", "")

    def update(self, value: "DeviceInfo"):
        if not isinstance(value, type(self)):
            raise TypeError("Can only update from another DeviceInfo")
        # pylint: disable=protected-access
        self._value = value._value
        return self


class DaylightSavingsTimeInfo(system.DaylightSavingsTimeInfo):
    """Dalight Savings Time Info"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        super().__init__()
        self._factory = factory

    @property
    def enabled(self):
        if (value := self._factory()) is None:
            return False
        return value.get("enable", False)

    @property
    def hour_offset(self):
        if (value := self._factory()) is None:
            return 0
        return value.get("offset", 0)

    class TimeInfo(system.DaylightSavingsTimeInfo.TimeInfo):
        """Time Info"""

        __slots__ = ("_factory", "_prefix")

        def __init__(self, factory: Callable[[], dict], prefix: str):
            super().__init__()
            self._factory = factory
            self._prefix = prefix

        def _get_value(self, key: str) -> int:
            if (value := self._factory()) is None:
                return 0
            return value.get(self._prefix + key, 0)

        @property
        def hour(self):
            return self._get_value("Hour")

        @property
        def minute(self):
            return self._get_value("Min")

        @property
        def month(self):
            return self._get_value("Mon")

        @property
        def week(self):
            return self._get_value("Week")

        @property
        def weekday(self):
            if (value := self._factory()) is None:
                return WeekDays.SUNDAY
            return _INT_WEEKDAY_MAP.get(
                value.get(self._prefix + "Weekday", 0), WeekDays.SUNDAY
            )

    @property
    def start(self):
        return type(self).TimeInfo(self._factory, "start")

    @property
    def end(self):
        return type(self).TimeInfo(self._factory, "end")


class TimeInfo(system.TimeInfo):
    """Device Time"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        super().__init__()
        self._factory = factory

    @property
    def year(self):
        if (value := self._factory()) is None:
            return 0
        return value.get("year", 0)

    @property
    def month(self):
        if (value := self._factory()) is None:
            return 0
        return value.get("mon", 0)

    @property
    def day(self):
        if (value := self._factory()) is None:
            return 0
        return value.get("day", 0)

    @property
    def hour(self):
        if (value := self._factory()) is None:
            return 0
        return value.get("hour", 0)

    @property
    def minute(self):
        if (value := self._factory()) is None:
            return 0
        return value.get("min", 0)

    @property
    def second(self):
        if (value := self._factory()) is None:
            return 0
        return value.get("sec", 0)

    @property
    def hour_format(self):
        if (value := self._factory()) is None:
            return typings.HourFormat.HR_12
        return value.get("hourFmt", typings.HourFormat.HR_12)

    @property
    def date_format(self):
        if (value := self._factory()) is None:
            return "DD/MM/YYYY"
        return value.get("timeFmt", "DD/MM/YYYY")

    @property
    def timezone_offset(self):
        if (value := self._factory()) is None:
            return 0
        return value.get("timeZone", 0)


_DEFAULT_STORAGETYPE: Final[typings.StorageTypes] = None


class StorageInfo(typings.StorageInfo):
    """REST Storage Info"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        super().__init__()
        self._factory = factory

    @property
    def id(self) -> bool:
        if (value := self._factory()) is None:
            return 0
        return value.get("number", 0)

    @property
    def capacity(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("capacity", 0)

    @property
    def formatted(self) -> bool:
        if (value := self._factory()) is None:
            return 0
        return value.get("format", 0)

    @property
    def mounted(self) -> bool:
        if (value := self._factory()) is None:
            return 0
        return value.get("mount", 0)

    @property
    def free_space(self) -> bool:
        if (value := self._factory()) is None:
            return 0
        return value.get("size", 0)

    @property
    def type(self):
        if (value := self._factory()) is None:
            return _DEFAULT_STORAGETYPE
        return _INT_STORAGETYPE_MAP.get(
            value.get("storageType", 0), _DEFAULT_STORAGETYPE
        )
