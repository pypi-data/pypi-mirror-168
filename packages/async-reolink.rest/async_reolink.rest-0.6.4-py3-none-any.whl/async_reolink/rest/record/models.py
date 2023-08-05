"""REST Record Models"""

from datetime import date, datetime, time
from typing import Callable, Final, Iterable, overload
from async_reolink.api.typings import DateTimeValue as BaseDateTimeValue, StreamTypes
from async_reolink.api.record import typings

from ..typings import STR_STREAMTYPES_MAP, STREAMTYPES_STR_MAP, FactoryValue

# pylint: disable=missing-function-docstring


class DateTimeValue(BaseDateTimeValue):
    """REST Recording DateTime Value"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    @property
    def year(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("year", 0)

    @property
    def month(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("mon", 0)

    @property
    def day(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("day", 0)

    def to_date(self):
        return date(self.year, self.month, self.day)

    @property
    def hour(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("hour", 0)

    @property
    def minute(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("min", 0)

    @property
    def second(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("sec", 0)

    def to_time(self):
        return time(self.hour, self.minute, self.second)

    def to_datetime(self):
        return datetime(self.to_date(), self.to_time())


class MutableDateTimeValue(DateTimeValue):
    """REST Recording Mutable DateTime Value"""

    __slots__ = ()

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, value: datetime) -> None:
        ...

    @overload
    def __init__(self, value: typings.DateTimeValue) -> None:
        ...

    @overload
    def __init__(self, factory: FactoryValue[dict]) -> None:
        ...

    def __init__(self, factory: FactoryValue[dict] = None) -> None:
        source: typings.DateTimeValue = None
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
            self.year = source.year
            self.month = source.month
            self.day = source.day
            self.hour = source.hour
            self.minute = source.minute
            self.second = source.second

    @property
    def _value(self):
        return self._factory(True)

    @DateTimeValue.year.setter
    def year(self, value):
        self._value["year"] = value

    @DateTimeValue.month.setter
    def month(self, value):
        self._value["mon"] = value

    @DateTimeValue.day.setter
    def day(self, value):
        self._value["day"] = value

    @DateTimeValue.hour.setter
    def hour(self, value):
        self._value["hour"] = value

    @DateTimeValue.minute.setter
    def minute(self, value):
        self._value["min"] = value

    @DateTimeValue.second.setter
    def second(self, value):
        self._value["sec"] = value


_DEFAULT_STREAMTYPE: Final = StreamTypes.MAIN
_DEFAULT_STREAMTYPE_STR = STREAMTYPES_STR_MAP[_DEFAULT_STREAMTYPE]


class Search(typings.Search):
    """REST Search"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    @property
    def status_only(self) -> bool:
        if (value := self._factory()) is None:
            return 0
        return value.get("onlyStatus", 0)

    @property
    def stream_type(self):
        if (value := self._factory()) is None:
            return _DEFAULT_STREAMTYPE
        return STR_STREAMTYPES_MAP[value.get("streamType", _DEFAULT_STREAMTYPE_STR)]

    def _get_start(self) -> dict:
        if (value := self._factory()) is None:
            return None
        return value.get("StartTime", None)

    @property
    def start(self):
        return DateTimeValue(self._get_start)

    def _get_end(self) -> dict:
        if (value := self._factory()) is None:
            return None
        return value.get("EndTime", None)

    @property
    def end(self):
        return DateTimeValue(self._get_end)


class MutableSearch(Search):
    """REST Mutable Search"""

    __slots__ = ()

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, value: typings.Search) -> None:
        ...

    @overload
    def __init__(self, factory: FactoryValue[dict]) -> None:
        ...

    def __init__(self, factory: FactoryValue[dict] = None) -> None:
        source: typings.Search = None
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
            self.status_only = source.status_only
            self.stream_type = source.stream_type
            self.start = source.start
            self.end = source.end

    @property
    def _value(self):
        return self._factory(True)

    @Search.status_only.setter
    def status_only(self, value):
        self._value["onlyStatus"] = int(bool(value))

    @Search.stream_type.setter
    def stream_type(self, value):
        self._value["streamType"] = STREAMTYPES_STR_MAP[value or _DEFAULT_STREAMTYPE]

    def _get_start(self, create=False) -> dict:
        _key: Final = "StartTime"
        if (value := self._factory(create)) is None:
            return None
        if _key in value or not create:
            return value.get(_key, None)
        return value.setdefault(_key, {})

    @property
    def start(self):
        return MutableDateTimeValue(self._get_start)

    @start.setter
    def start(self, value: typings.DateTimeValue):
        if not isinstance(value, MutableDateTimeValue):
            value = MutableDateTimeValue(value)
        self._value["StartTime"] = value._factory(True)

    def _get_end(self, create=False) -> dict:
        _key: Final = "EndTime"
        if (value := self._factory(create)) is None:
            return None
        if _key in value or not create:
            return value.get(_key, None)
        return value.setdefault(_key, {})

    @property
    def end(self):
        return MutableDateTimeValue(self._get_end)

    @end.setter
    def end(self, value: typings.DateTimeValue):
        if not isinstance(value, MutableDateTimeValue):
            value = MutableDateTimeValue(value)
        self._value["EndTime"] = value._factory(True)


class File(typings.File):
    """REST Recording File"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    def _get_start(self) -> dict:
        if (value := self._factory()) is None:
            return None
        return value.get("StartTime", None)

    @property
    def frame_rate(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("frameRate", 0)

    @property
    def width(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("width", 0)

    @property
    def height(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("height", 0)

    @property
    def size(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("size", 0)

    @property
    def name(self) -> str:
        if (value := self._factory()) is None:
            return 0
        return value.get("name", 0)

    @property
    def type(self) -> str:
        if (value := self._factory()) is None:
            return 0
        return value.get("type", 0)

    @property
    def start(self):
        return DateTimeValue(self._get_start)

    def _get_end(self) -> dict:
        if (value := self._factory()) is None:
            return None
        return value.get("EndTime", None)

    @property
    def end(self):
        return DateTimeValue(self._get_end)


class _SearchStatusTable(Iterable[int]):
    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    def __iter__(self):
        if (value := self._factory()) is None:
            return
        for i, _c in enumerate(str(value), 1):
            if _c == "1":
                yield i


class SearchStatus(typings.SearchStatus):
    """REST Recodring Search Status"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    @property
    def year(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("year", 0)

    @property
    def month(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("mon", 0)

    def _get_table(self) -> str:
        if (value := self._factory()) is None:
            return ""
        return value.get("table", "")

    @property
    def days(self):
        return _SearchStatusTable(self._get_table)

    def __iter__(self):
        year = self.year
        month = self.month
        for _d in self.days:
            yield date(year, month, _d)
