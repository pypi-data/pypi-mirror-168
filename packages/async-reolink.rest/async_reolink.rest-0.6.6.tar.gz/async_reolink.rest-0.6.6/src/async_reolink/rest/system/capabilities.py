"""System capabilities"""

from enum import Flag
from functools import reduce
from itertools import chain, combinations
from types import MappingProxyType
from typing import Callable, Final, Mapping, TypeVar, overload
from async_reolink.api.system import capabilities

_T = TypeVar("_T")

# pylint: disable=too-few-public-methods
# pylint: disable=missing-function-docstring

_defaults: dict[type, any] = {None: 0}

_F = TypeVar("_F", bound=Flag)


def _flag_map(__flag_map: dict[int, _F]):
    def bor(a: _T, b: _T) -> _T:
        return a | b

    lookup = {_v: _k for _k, _v in __flag_map.items()}
    values = list(__flag_map.values())
    for t in chain.from_iterable(
        combinations(values, i) for i in range(len(values) + 1)
    ):
        if len(t) == 0:
            continue
        vt = map(lambda f: lookup[f], t)
        f = reduce(bor, t)
        v = reduce(bor, vt)
        __flag_map[v] = f

    return __flag_map


def _map_factory(__map: dict[int, _T], __default: _T = None) -> Callable[[int], _T]:
    if __default is None and 0 in __map:
        __default = __map[0]

    def _factory(value: int):
        return __map.get(value, __default)

    _defaults[_factory] = __default
    return _factory


_INT_PERMISSION_MAP: Final = MappingProxyType(
    _flag_map(
        {
            1: capabilities.Permissions.OPTION,
            2: capabilities.Permissions.WRITE,
            4: capabilities.Permissions.READ,
        }
    )
)
_NO_PERMISSIONS: capabilities.Permissions = None


class Capability(capabilities.Capability[_T]):
    """Capability"""

    __slots__ = ("_factory", "_init")

    @overload
    def __init__(self: "Capability[int]", factory: Callable[[], dict] = None):
        ...

    @overload
    def __init__(
        self: "Capability[_T]", factory: Callable[[], dict], __type: Callable[[int], _T]
    ) -> None:
        ...

    def __init__(
        self, factory: Callable[[], dict], __type: Callable[[int], _T] = None
    ) -> None:
        super().__init__()
        self._factory = factory
        self._init = __type
        if __type not in _defaults:
            _defaults[__type] = __type(0)

    def _get_value(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("ver", 0)

    @property
    def value(self) -> _T:
        value = self._get_value()
        if value == 0:
            return _defaults[self._init]
        if self._init is not None:
            return self._init(value)
        return value

    @property
    def permissions(self):
        if (value := self._factory()) is None:
            return _NO_PERMISSIONS
        return _INT_PERMISSION_MAP.get(value.get("permit", 0), _NO_PERMISSIONS)

    def __bool__(self):
        if self.permissions is None:
            return False
        return bool(self._get_value())

    def __index__(self):
        return self._get_value()

    def __int__(self):
        return self._get_value()

    def __str__(self):
        return str(self.value)

    def __eq__(self, __o: object) -> bool:
        if hasattr(__o, "__index__"):
            return self._get_value() == __o.__index__()
        return self.value == __o

    def __repr__(self):
        return f"<{self.__class__.__name__}: {repr(self._factory())}>"


_INT_CLOUDSTORAGE: Final = _map_factory(
    _flag_map(
        {
            1 << 0: capabilities.CloudStorage.UPLOAD,
            1 << 1: capabilities.CloudStorage.CONFIG,
            1 << 3: capabilities.CloudStorage.DEPLOY,
        }
    )
)

_INT_DAYNIGHT: Final = _map_factory(
    {1: capabilities.DayNight.DAY_NIGHT, 2: capabilities.DayNight.THRESHOLD}
)

_INT_DDNS: Final = _map_factory(
    {
        1: capabilities.DDns.SWAN,
        2: capabilities.DDns.THREE322,
        3: capabilities.DDns.DYNDNS,
        4: capabilities.DDns.SWAN_3322,
        5: capabilities.DDns.SWAN_DYNDNS,
        6: capabilities.DDns.DYNDNS_3322,
        7: capabilities.DDns.SWAN_DYNDNS_3322,
        8: capabilities.DDns.NOIP,
        9: capabilities.DDns.DYNDNS_NOIP,
    }
)

_INT_EMAIL: Final = _map_factory(
    {
        1: capabilities.Email.JPEG,
        2: capabilities.Email.VIDEO_JPEG,
        3: capabilities.Email.VIDEO_JPEG_NICK,
    }
)

_INT_ENCODINGTYPE: Final = _map_factory(
    {0: capabilities.EncodingType.H264, 1: capabilities.EncodingType.H265}
)

_INT_FLOODLIGHT: Final = _map_factory(
    {1: capabilities.FloodLight.WHITE, 2: capabilities.FloodLight.AUTO}
)

_INT_FTP: Final = _map_factory(
    {
        1: capabilities.Ftp.STREAM,
        2: capabilities.Ftp.JPEG_STREAM,
        3: capabilities.Ftp.MODE,
        4: capabilities.Ftp.JPEG_STREAM_MODE,
        5: capabilities.Ftp.STREAM_MODE_TYPE,
        6: capabilities.Ftp.JPEG_STREAM_MODE_TYPE,
    }
)

_INT_LIVE: Final = _map_factory(
    {1: capabilities.Live.MAIN_EXTERN_SUB, 2: capabilities.Live.MAIN_SUB}
)

_INT_OSD: Final = _map_factory(
    {1: capabilities.Osd.SUPPORTED, 2: capabilities.Osd.DISTINCT}
)

_INT_PTZCONTROL: Final = _map_factory(
    {1: capabilities.PTZControl.ZOOM, 2: capabilities.PTZControl.ZOOM_FOCUS}
)

_INT_PTZDIRECTION: Final = _map_factory(
    {0: capabilities.PTZDirection.EIGHT_AUTO, 1: capabilities.PTZDirection.FOUR_NO_AUTO}
)

_INT_PTZTYPE: Final = _map_factory(
    {
        1: capabilities.PTZType.AF,
        2: capabilities.PTZType.PTZ,
        3: capabilities.PTZType.PT,
        4: capabilities.PTZType.BALL,
        5: capabilities.PTZType.PTZ_NO_SPEED,
    }
)

_INT_RECORDSCHEDULE: Final = _map_factory(
    {1: capabilities.RecordSchedule.MOTION, 2: capabilities.RecordSchedule.MOTION_LIVE}
)

_INT_SCHEDULEVERSION: Final = _map_factory(
    {0: capabilities.ScheduleVersion.BASIC, 1: capabilities.ScheduleVersion.V20}
)

_INT_TIME: Final = _map_factory(
    {
        1: capabilities.Time.SUNDAY,
        2: capabilities.Time.ANYDAY,
    }
)

_INT_UPGRADE: Final = _map_factory(
    {1: capabilities.Upgrade.MANUAL, 2: capabilities.Upgrade.ONLINE}
)

_INT_VIDEOCLIP: Final = _map_factory(
    {1: capabilities.VideoClip.FIXED, 2: capabilities.VideoClip.MOD}
)


class ChannelCapabilities(capabilities.ChannelCapabilities):
    """Channel Capabilities"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        super().__init__()
        self._factory = factory

    def _keyed_factory(self, key: str):
        def _factory() -> dict:
            if (value := self._factory()) is None:
                return None
            return value.get(key, None)

        return _factory

    class AI(capabilities.ChannelCapabilities.AI):
        """AI"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        class Track(capabilities.ChannelCapabilities.AI.Track):
            """Track"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            def _keyed_factory(self, key: str):
                def _factory() -> dict:
                    if (value := self._factory()) is None:
                        return None
                    return value.get(key, None)

                return _factory

            @property
            def _value(self):
                return Capability(self._keyed_factory("aiTrack"))

            def __bool__(self):
                return self._value.__bool__()

            def __index__(self):
                return self._value.__index__()

            def __int__(self):
                return self._value.__int__()

            def __str__(self):
                return self._value.__str__()

            def __eq__(self, __o: object):
                return self._value.__eq__(__o)

            @property
            def value(self):
                return self._value.value

            @property
            def permissions(self):
                return self._value.permissions

            @property
            def pet(self):
                return Capability(self._keyed_factory("aiTrackDogCat"))

        @property
        def track(self):
            return type(self).Track(self._factory)

    @property
    def ai(self):
        return type(self).AI(self._factory)

    class Alarm(capabilities.ChannelCapabilities.Alarm):
        """Alarm"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        def _keyed_factory(self, key: str):
            def _factory() -> dict:
                if (value := self._factory()) is None:
                    return None
                return value.get(key, None)

            return _factory

        @property
        def audio(self):
            return Capability(self._keyed_factory("alarmAudio"))

        @property
        def io_in(self):
            return Capability(self._keyed_factory("alarmIoIn"))

        @property
        def io_out(self):
            return Capability(self._keyed_factory("alarmIoOut"))

        @property
        def motion(self):
            return Capability(self._keyed_factory("alarmMd"))

        @property
        def rf(self):
            return Capability(self._keyed_factory("alarmRf"))

    @property
    def alarm(self):
        return type(self).Alarm(self._factory)

    @property
    def battery(self):
        return Capability(self._keyed_factory("battery"))

    @property
    def battery_analysis(self):
        return Capability(self._keyed_factory("batAnalysis"))

    @property
    def camera_mode(self):
        return Capability(self._keyed_factory("cameraMode"))

    @property
    def disable_autofocus(self):
        return Capability(self._keyed_factory("disableAutoFocus"))

    @property
    def enc(self):
        return Capability(self._keyed_factory("enc"))

    @property
    def floodlight(self):
        return Capability(self._keyed_factory("floodLight"), _INT_FLOODLIGHT)

    @property
    def ftp(self):
        return Capability(self._keyed_factory("ftp"), _INT_FTP)

    @property
    def image(self):
        return Capability(self._keyed_factory("image"))

    @property
    def indicator_light(self):
        return Capability(self._keyed_factory("indicatorLight"))

    class ISP(capabilities.ChannelCapabilities.ISP):
        """ISP"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        def _keyed_factory(self, key: str):
            def _factory() -> dict:
                if (value := self._factory()) is None:
                    return None
                return value.get(key, None)

            return _factory

        @property
        def _value(self):
            return Capability(self._keyed_factory("isp"))

        def __bool__(self):
            return self._value.__bool__()

        def __index__(self):
            return self._value.__index__()

        def __int__(self):
            return self._value.__int__()

        def __str__(self):
            return self._value.__str__()

        def __eq__(self, __o: object):
            return self._value.__eq__(__o)

        @property
        def value(self):
            return self._value.value

        @property
        def permissions(self):
            return self._value.permissions

        @property
        def threeDnr(self):
            return Capability(self._keyed_factory("isp3Dnr"))

        @property
        def antiflicker(self):
            return Capability(self._keyed_factory("ispAntiFlick"))

        @property
        def backlight(self):
            return Capability(self._keyed_factory("ispBackLight"))

        @property
        def bright(self):
            return Capability(self._keyed_factory("ispBright"))

        @property
        def contrast(self):
            return Capability(self._keyed_factory("ispContrast"))

        @property
        def day_night(self):
            return Capability(self._keyed_factory("ispDayNight"), _INT_DAYNIGHT)

        @property
        def exposure_mode(self):
            return Capability(self._keyed_factory("ispExposureMode"))

        @property
        def flip(self):
            return Capability(self._keyed_factory("ispFlip"))

        @property
        def hue(self):
            return Capability(self._keyed_factory("ispHue"))

        @property
        def mirror(self):
            return Capability(self._keyed_factory("ispMirror"))

        @property
        def satruation(self):
            return Capability(self._keyed_factory("ispSatruation"))

        @property
        def sharpen(self):
            return Capability(self._keyed_factory("ispSharpen"))

        @property
        def white_balance(self):
            return Capability(self._keyed_factory("ispWhiteBalance"))

    @property
    def isp(self):
        return type(self).ISP(self._factory)

    @property
    def led_control(self):
        return Capability(self._keyed_factory("ledControl"))

    @property
    def live(self):
        return Capability(self._keyed_factory("live"), _INT_LIVE)

    @property
    def main_encoding(self):
        return Capability(self._keyed_factory("mainEncType"), _INT_ENCODINGTYPE)

    @property
    def mask(self):
        return Capability(self._keyed_factory("mask"))

    class MD(capabilities.ChannelCapabilities.MD):
        """MotionDetection"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        def _keyed_factory(self, key: str):
            def _factory() -> dict:
                if (value := self._factory()) is None:
                    return None
                return value.get(key, None)

            return _factory

        class Trigger(capabilities.ChannelCapabilities.MD.Trigger):
            """Trigger"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            def _keyed_factory(self, key: str):
                def _factory() -> dict:
                    if (value := self._factory()) is None:
                        return None
                    return value.get(key, None)

                return _factory

            @property
            def audio(self):
                return Capability(self._keyed_factory("mdTriggerAudio"))

            @property
            def record(self):
                return Capability(self._keyed_factory("mdTriggerRecord"))

        @property
        def trigger(self):
            return type(self).Trigger(self._factory)

        @property
        def with_pir(self):
            return Capability(self._keyed_factory("mdWithPir"))

    @property
    def motion_detection(self):
        return type(self).MD(self._factory)

    @property
    def osd(self):
        return Capability(self._keyed_factory("osd"), _INT_OSD)

    @property
    def power_led(self):
        return Capability(self._keyed_factory("powerLed"))

    class PTZ(capabilities.ChannelCapabilities.PTZ):
        """PTZ"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        def _keyed_factory(self, key: str):
            def _factory() -> dict:
                if (value := self._factory()) is None:
                    return None
                return value.get(key, None)

            return _factory

        @property
        def control(self):
            return Capability(self._keyed_factory("ptzCtrl"), _INT_PTZCONTROL)

        @property
        def direction(self):
            return Capability(self._keyed_factory("ptzDirection"), _INT_PTZDIRECTION)

        @property
        def patrol(self):
            return Capability(self._keyed_factory("ptzPatrol"))

        @property
        def preset(self):
            return Capability(self._keyed_factory("ptzPreset"))

        @property
        def tattern(self):
            return Capability(self._keyed_factory("ptzTattern"))

        @property
        def type(self):
            return Capability(self._keyed_factory("ptzType"), _INT_PTZTYPE)

    @property
    def ptz(self):
        return type(self).PTZ(self._factory)

    class Record(capabilities.ChannelCapabilities.Record):
        """Record"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        def _keyed_factory(self, key: str):
            def _factory() -> dict:
                if (value := self._factory()) is None:
                    return None
                return value.get(key, None)

            return _factory

        @property
        def config(self):
            return Capability(self._keyed_factory("recCfg"))

        @property
        def download(self):
            return Capability(self._keyed_factory("recDownload"))

        @property
        def replay(self):
            return Capability(self._keyed_factory("recReplay"))

        @property
        def schedule(self):
            return Capability(self._keyed_factory("recSchedule"), _INT_RECORDSCHEDULE)

    @property
    def record(self):
        return type(self).Record(self._factory)

    @property
    def shelter_config(self):
        return Capability(self._keyed_factory("shelterCfg"))

    @property
    def snap(self):
        return Capability(self._keyed_factory("snap"))

    class Supports(capabilities.ChannelCapabilities.Supports):
        """Supports"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        def _keyed_factory(self, key: str):
            def _factory() -> dict:
                if (value := self._factory()) is None:
                    return None
                return value.get(key, None)

            return _factory

        class AI(capabilities.ChannelCapabilities.Supports.AI):
            """AI"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            def _keyed_factory(self, key: str):
                def _factory() -> dict:
                    if (value := self._factory()) is None:
                        return None
                    return value.get(key, None)

                return _factory

            @property
            def _value(self):
                return Capability(self._keyed_factory("supportAi"))

            def __bool__(self):
                return self._value.__bool__()

            def __index__(self):
                return self._value.__index__()

            def __int__(self):
                return self._value.__int__()

            def __str__(self):
                return self._value.__str__()

            def __eq__(self, __o: object):
                return self._value.__eq__(__o)

            @property
            def value(self):
                return self._value.value

            @property
            def permissions(self):
                return self._value.permissions

            @property
            def animal(self):
                return Capability(self._keyed_factory("supportAiAnimal"))

            @property
            def detect_config(self):
                return Capability(self._keyed_factory("supportAiDetectConfig"))

            @property
            def pet(self):
                return Capability(self._keyed_factory("supportAiDogCat"))

            @property
            def face(self):
                return Capability(self._keyed_factory("supportAiFace"))

            @property
            def people(self):
                return Capability(self._keyed_factory("supportAiPeople"))

            @property
            def sensitivity(self):
                return Capability(self._keyed_factory("supportAiSensitivity"))

            @property
            def stay_time(self):
                return Capability(self._keyed_factory("supportAiStayTime"))

            @property
            def target_size(self):
                return Capability(self._keyed_factory("supportAiTargetSize"))

            @property
            def track_classify(self):
                return Capability(self._keyed_factory("supportAiTrackClassify"))

            @property
            def vehicle(self):
                return Capability(self._keyed_factory("supportAiVehicle"))

            @property
            def adjust(self):
                return Capability(self._keyed_factory("supportAoAdjust"))

        @property
        def ai(self):
            return type(self).AI(self._factory)

        class FloodLight(capabilities.ChannelCapabilities.Supports.FloodLight):
            """FloodLight"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            def _keyed_factory(self, key: str):
                def _factory() -> dict:
                    if (value := self._factory()) is None:
                        return None
                    return value.get(key, None)

                return _factory

            @property
            def brightness(self):
                return Capability(self._keyed_factory("supportFLBrightness"))

            @property
            def intelligent(self):
                return Capability(self._keyed_factory("supportFLIntelligent"))

            @property
            def keep_on(self):
                return Capability(self._keyed_factory("supportFLKeepOn"))

            @property
            def schedule(self):
                return Capability(self._keyed_factory("supportFLSchedule"))

            @property
            def switch(self):
                return Capability(self._keyed_factory("supportFLswitch"))

        @property
        def flood_light(self):
            return type(self).FloodLight(self._factory)

        @property
        def gop(self):
            return Capability(self._keyed_factory("supportGop"))

        @property
        def motion_detection(self):
            return Capability(self._keyed_factory("supportMd"))

        @property
        def ptz_check(self):
            return Capability(self._keyed_factory("supportPtzCheck"))

        @property
        def threshold_adjust(self):
            return Capability(self._keyed_factory("supportThresholdAdjust"))

        @property
        def white_dark(self):
            return Capability(self._keyed_factory("supportWhiteDark"))

    @property
    def supports(self):
        return type(self).Supports(self._factory)

    @property
    def video_clip(self):
        return Capability(self._keyed_factory("videoClip"), _INT_VIDEOCLIP)

    @property
    def watermark(self):
        return Capability(self._keyed_factory("waterMark"))

    @property
    def white_balance(self):
        return Capability(self._keyed_factory("white_balance"))

    def __repr__(self):
        return f"<{self.__class__.__name__}: {repr(self._factory())}>"


class _Channels(Mapping[int, ChannelCapabilities]):
    """Channels"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], list]) -> None:
        super().__init__()
        self._factory = factory

    def __getitem__(self, __k: int):
        def _get():
            if (_list := self._factory()) is None:
                return None
            return _list[__k]

        return ChannelCapabilities(_get)

    def __iter__(self):
        if (_list := self._factory()) is None:
            return
        for i in range(0, len(_list)):
            yield i

    def __len__(self):
        if (_list := self._factory()) is None:
            return 0
        return len(_list)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {repr(self._factory())}>"


class Capabilities(capabilities.Capabilities):
    """Capabilities"""

    __slots__ = ("_value",)

    def __init__(self, value: dict) -> None:
        super().__init__()
        self._value = value

    def _factory(self):
        return self._value

    def _keyed_factory(self, key: str):
        def _factory() -> dict:
            return self._value.get(key, None)

        return _factory

    @property
    def three_g(self):
        return Capability(self._keyed_factory("3g"))

    @property
    def channels(self):
        """channels"""
        return _Channels(self._keyed_factory("abilityChn"))

    class Alarm(capabilities.Capabilities.Alarm):
        """Alarm"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        def _keyed_factory(self, key: str):
            def _factory() -> dict:
                if (value := self._factory()) is None:
                    return None
                return value.get(key, None)

            return _factory

        @property
        def audio(self):
            return Capability(self._keyed_factory("alarmAudio"))

        @property
        def disconnect(self):
            return Capability(self._keyed_factory("alarmDisconnet"))

        class HDD(capabilities.Capabilities.Alarm.HDD):
            """HDDD"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            def _keyed_factory(self, key: str):
                def _factory() -> dict:
                    if (value := self._factory()) is None:
                        return None
                    return value.get(key, None)

                return _factory

            @property
            def error(self):
                return Capability(self._keyed_factory("alarmHddErr"))

            @property
            def full(self):
                return Capability(self._keyed_factory("alarmHddFull"))

        @property
        def hdd(self):
            return type(self).HDD(self._factory)

        @property
        def ip_conflict(self):
            return Capability(self._keyed_factory("alarmIpConflict"))

    @property
    def alarm(self):
        return type(self).Alarm(self._factory)

    @property
    def auth(self):
        return Capability(self._keyed_factory("auth"))

    @property
    def auto_maintenance(self):
        return Capability(self._keyed_factory("autoMaint"))

    @property
    def cloud_storage(self):
        return Capability(self._keyed_factory("cloudStorage"), _INT_CLOUDSTORAGE)

    @property
    def custom_audio(self):
        return Capability(self._keyed_factory("customAudio"))

    @property
    def date_format(self):
        return Capability(self._keyed_factory("dateFormat"))

    @property
    def ddns(self):
        return Capability(self._keyed_factory("ddns"), _INT_DDNS)

    class Device(capabilities.Capabilities.Device):
        """Device"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        def _keyed_factory(self, key: str):
            def _factory() -> dict:
                if (value := self._factory()) is None:
                    return None
                return value.get(key, None)

            return _factory

        @property
        def info(self):
            return Capability(self._keyed_factory("devInfo"))

        @property
        def name(self):
            return Capability(self._keyed_factory("devName"))

    @property
    def device(self):
        return type(self).Device(self._factory)

    @property
    def disable_autofocus(self):
        return Capability(self._keyed_factory("disableAutoFocus"))

    @property
    def disk(self):
        return Capability(self._keyed_factory("disk"))

    @property
    def display(self):
        return Capability(self._keyed_factory("display"))

    class Email(capabilities.Capabilities.Email):
        """Email"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        def _keyed_factory(self, key: str):
            def _factory() -> dict:
                if (value := self._factory()) is None:
                    return None
                return value.get(key, None)

            return _factory

        @property
        def _value(self):
            return Capability(self._keyed_factory("email"), _INT_EMAIL)

        @property
        def value(self):
            return self._value.value

        @property
        def permissions(self):
            return self._value.permissions

        def __bool__(self):
            return bool(self.value)

        @property
        def interval(self):
            return Capability(self._keyed_factory("emailInterval"))

        @property
        def schedule(self):
            return Capability(self._keyed_factory("emailSchedule"))

    @property
    def email(self):
        return type(self).Email(self._factory)

    @property
    def config_import(self):
        return Capability(self._keyed_factory("importCfg"))

    @property
    def config_export(self):
        return Capability(self._keyed_factory("exportCfg"))

    class FTP(capabilities.Capabilities.FTP):
        """FTP"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        def _keyed_factory(self, key: str):
            def _factory() -> dict:
                if (value := self._factory()) is None:
                    return None
                return value.get(key, None)

            return _factory

        @property
        def auto_dir(self):
            return Capability(self._keyed_factory("ftpAutoDir"))

        class Stream(capabilities.Capabilities.FTP.Stream):
            """Stream"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            def _keyed_factory(self, key: str):
                def _factory() -> dict:
                    if (value := self._factory()) is None:
                        return None
                    return value.get(key, None)

                return _factory

            @property
            def ext(self):
                return Capability(self._keyed_factory("ftpExtStream"))

            @property
            def sub(self):
                return Capability(self._keyed_factory("ftpSubStream"))

        @property
        def stream(self):
            return type(self).Stream(self._factory)

        @property
        def picture(self):
            return Capability(self._keyed_factory("ftpPic"))

        @property
        def test(self):
            return Capability(self._keyed_factory("ftpTest"))

    @property
    def ftp(self):
        return type(self).FTP(self._factory)

    @property
    def hour_format(self):
        """change hour format supported"""

        return Capability(self._keyed_factory("hourFmt"))

    @property
    def http(self):
        return Capability(self._keyed_factory("http"))

    @property
    def http_flv(self):
        return Capability(self._keyed_factory("httpFlv"))

    @property
    def https(self):
        return Capability(self._keyed_factory("https"))

    @property
    def ipc_manager(self):
        return Capability(self._keyed_factory("ipcManager"))

    @property
    def led_control(self):
        return Capability(self._keyed_factory("ledControl"))

    @property
    def local_link(self):
        return Capability(self._keyed_factory("localLink"))

    @property
    def log(self):
        return Capability(self._keyed_factory("log"))

    @property
    def media_port(self):
        return Capability(self._keyed_factory("mediaPort"))

    @property
    def ntp(self):
        return Capability(self._keyed_factory("ntp"))

    @property
    def online(self):
        return Capability(self._keyed_factory("online"))

    @property
    def onvif(self):
        return Capability(self._keyed_factory("onvif"))

    @property
    def p2p(self):
        return Capability(self._keyed_factory("p2p"))

    @property
    def performance(self):
        return Capability(self._keyed_factory("performance"))

    @property
    def pppoe(self):
        return Capability(self._keyed_factory("pppoe"))

    @property
    def push(self):
        return Capability(self._keyed_factory("push"))

    @property
    def push_schedule(self):
        return Capability(self._keyed_factory("pushSchedule"))

    @property
    def reboot(self):
        return Capability(self._keyed_factory("reboot"))

    class Record(capabilities.Capabilities.Record):
        """Record"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        def _keyed_factory(self, key: str):
            def _factory() -> dict:
                if (value := self._factory()) is None:
                    return None
                return value.get(key, None)

            return _factory

        @property
        def extension_time_list(self):
            return Capability(self._keyed_factory("recExtensionTimeList"))

        @property
        def overwrite(self):
            return Capability(self._keyed_factory("recOverWrite"))

        @property
        def pack_duration(self):
            return Capability(self._keyed_factory("recPackDuration"))

        @property
        def pre_record(self):
            return Capability(self._keyed_factory("recPreRecord"))

    @property
    def record(self):
        return type(self).Record(self._factory)

    @property
    def restore(self):
        return Capability(self._keyed_factory("restore"))

    @property
    def rtmp(self):
        return Capability(self._keyed_factory("rtmp"))

    @property
    def rtsp(self):
        return Capability(self._keyed_factory("rtsp"))

    @property
    def schedule_version(self):
        return Capability(self._keyed_factory("scheduleVersion"), _INT_SCHEDULEVERSION)

    @property
    def sd_card(self):
        return Capability(self._keyed_factory("sdCard"))

    @property
    def show_qr_code(self):
        return Capability(self._keyed_factory("showQrCode"))

    @property
    def sim_module(self):
        return Capability(self._keyed_factory("simModule"))

    class Supports(capabilities.Capabilities.Supports):
        """Supports"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        class Audio(capabilities.Capabilities.Supports.Audio):
            """Audio"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            class Alarm(capabilities.Capabilities.Supports.Audio.Alarm):
                """Alarm"""

                __slots__ = ("_factory",)

                def __init__(self, factory: Callable[[], dict]) -> None:
                    super().__init__()
                    self._factory = factory

                def _keyed_factory(self, key: str):
                    def _factory() -> dict:
                        if (value := self._factory()) is None:
                            return None
                        return value.get(key, None)

                    return _factory

                @property
                def _value(self):
                    return Capability(self._keyed_factory("supportAudioAlarm"))

                @property
                def value(self):
                    return self._value.value

                @property
                def permissions(self):
                    return self._value.permissions

                def __bool__(self):
                    return bool(self.value)

                @property
                def enable(self):
                    return Capability(self._keyed_factory("supportAudioAlarmEnable"))

                @property
                def schedule(self):
                    return Capability(self._keyed_factory("supportAudioAlarmSchedule"))

                @property
                def task_enable(self):
                    return Capability(
                        self._keyed_factory("supportAudioAlarmTaskEnable")
                    )

            @property
            def alarm(self):
                return type(self).Alarm(self._factory)

        @property
        def audio(self):
            return type(self).Audio(self._factory)

        class Buzzer(capabilities.Capabilities.Supports.Buzzer):
            """Buzzer"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            class Task(capabilities.Capabilities.Supports.Buzzer.Task):
                """Task"""

                __slots__ = ("_factory",)

                def __init__(self, factory: Callable[[], dict]) -> None:
                    super().__init__()
                    self._factory = factory

                def _keyed_factory(self, key: str):
                    def _factory() -> dict:
                        if (value := self._factory()) is None:
                            return None
                        return value.get(key, None)

                    return _factory

                @property
                def _value(self):
                    return Capability(self._keyed_factory("supportBuzzerTask"))

                @property
                def value(self):
                    return self._value.value

                @property
                def permissions(self):
                    return self._value.permissions

                def __bool__(self):
                    return bool(self.value)

                @property
                def enable(self):
                    return Capability(self._keyed_factory("supportBuzzerEnable"))

            def _keyed_factory(self, key: str):
                def _factory() -> dict:
                    if (value := self._factory()) is None:
                        return None
                    return value.get(key, None)

                return _factory

            @property
            def _value(self):
                return Capability(self._keyed_factory("supportBuzzer"))

            @property
            def task(self):
                return type(self).Task(self._factory)

            @property
            def value(self):
                """value"""
                return self._value.value

            @property
            def permissions(self):
                """permissions"""
                return self._value.permissions

        @property
        def buzzer(self):
            return type(self).Buzzer(self._factory)

        class Email(capabilities.Capabilities.Supports.Email):
            """Email"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            def _keyed_factory(self, key: str):
                def _factory() -> dict:
                    if (value := self._factory()) is None:
                        return None
                    return value.get(key, None)

                return _factory

            @property
            def enable(self):
                return Capability(self._keyed_factory("supportEmailEnable"))

            @property
            def task_enable(self):
                return Capability(self._keyed_factory("supportEmailTaskEnable"))

        @property
        def email(self):
            return type(self).Email(self._factory)

        class FTP(capabilities.Capabilities.Supports.FTP):
            """FTP"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            class Cover(capabilities.Capabilities.Supports.FTP.Cover):
                """Cover"""

                __slots__ = ("_factory",)

                def __init__(self, factory: Callable[[], dict]) -> None:
                    super().__init__()
                    self._factory = factory

                def _keyed_factory(self, key: str):
                    def _factory() -> dict:
                        if (value := self._factory()) is None:
                            return None
                        return value.get(key, None)

                    return _factory

                @property
                def picture(self):
                    return Capability(self._keyed_factory("supportFtpCoverPicture"))

                @property
                def video(self):
                    return Capability(self._keyed_factory("supportFtpCoverVideo"))

            def _keyed_factory(self, key: str):
                def _factory() -> dict:
                    if (value := self._factory()) is None:
                        return None
                    return value.get(key, None)

                return _factory

            @property
            def cover(self):
                return type(self).Cover(self._factory)

            @property
            def dir_YM(self):
                return Capability(self._keyed_factory("supportFtpDirYM"))

            @property
            def enable(self):
                return Capability(self._keyed_factory("supportFtpEnable"))

            class Picture(capabilities.Capabilities.Supports.FTP.Picture):
                """Picture"""

                __slots__ = ("_factory",)

                def __init__(self, factory: Callable[[], dict]) -> None:
                    super().__init__()
                    self._factory = factory

                def _keyed_factory(self, key: str):
                    def _factory() -> dict:
                        if (value := self._factory()) is None:
                            return None
                        return value.get(key, None)

                    return _factory

                @property
                def capture_mode(self):
                    return Capability(self._keyed_factory("supportFtpPicCaptureMode"))

                @property
                def custom_resolution(self):
                    return Capability(self._keyed_factory("supportFtpPicResoCustom"))

                @property
                def swap(self):
                    return Capability(self._keyed_factory("supportFtpPictureSwap"))

            @property
            def picture(self):
                return type(self).Picture(self._factory)

            class Task(capabilities.Capabilities.Supports.FTP.Task):
                """Task"""

                __slots__ = ("_factory",)

                def __init__(self, factory: Callable[[], dict]) -> None:
                    super().__init__()
                    self._factory = factory

                def _keyed_factory(self, key: str):
                    def _factory() -> dict:
                        if (value := self._factory()) is None:
                            return None
                        return value.get(key, None)

                    return _factory

                @property
                def _value(self):
                    return Capability(self._keyed_factory("supportFtpTask"))

                @property
                def value(self):
                    return self._value.value

                @property
                def permissions(self):
                    return self._value.permissions

                def __bool__(self):
                    return bool(self.value)

                @property
                def enable(self):
                    return Capability(self._keyed_factory("supportFtpTaskEnable"))

            def _keyed_factory(self, key: str):
                def _factory() -> dict:
                    if (value := self._factory()) is None:
                        return None
                    return value.get(key, None)

                return _factory

            @property
            def task(self):
                return type(self).Task(self._factory)

            @property
            def video_swap(self):
                return Capability(self._keyed_factory("supportFtpVideoSwap"))

            @property
            def ftps_encrypt(self):
                return Capability(self._keyed_factory("supportFtpsEncrypt"))

        def _keyed_factory(self, key: str):
            def _factory() -> dict:
                if (value := self._factory()) is None:
                    return None
                return value.get(key, None)

            return _factory

        @property
        def ftp(self):
            return type(self).FTP(self._factory)

        @property
        def http_enable(self):
            return Capability(self._keyed_factory("supportHttpEnable"))

        @property
        def https_enable(self):
            return Capability(self._keyed_factory("supportHttpsEnable"))

        @property
        def onvif_enable(self):
            return Capability(self._keyed_factory("supportOnvifEnable"))

        @property
        def push_interval(self):
            return Capability(self._keyed_factory("supportPushInterval"))

        class Record(capabilities.Capabilities.Supports.Record):
            """Record"""

            __slots__ = ("_factory",)

            def __init__(self, factory: Callable[[], dict]) -> None:
                super().__init__()
                self._factory = factory

            def _keyed_factory(self, key: str):
                def _factory() -> dict:
                    if (value := self._factory()) is None:
                        return None
                    return value.get(key, None)

                return _factory

            @property
            def schedule_enable(self):
                return Capability(self._keyed_factory("supportRecScheduleEnable"))

            @property
            def enable(self):
                return Capability(self._keyed_factory("supportRecordEnable"))

        @property
        def record(self):
            return type(self).Record(self._factory)

        @property
        def rtmp_enable(self):
            return Capability(self._keyed_factory("supportRtmpEnable"))

        @property
        def rtsp_enable(self):
            return Capability(self._keyed_factory("supportRtspEnable"))

    @property
    def supports(self):
        return type(self).Supports(self._factory)

    @property
    def talk(self):
        return Capability(self._keyed_factory("talk"))

    @property
    def time(self):
        return Capability(self._keyed_factory("time"), _INT_TIME)

    @property
    def tv_system(self):
        return Capability(self._keyed_factory("tvSystem"))

    @property
    def upgrade(self):
        return Capability(self._keyed_factory("upgrade"), _INT_UPGRADE)

    @property
    def upnp(self):
        return Capability(self._keyed_factory("upnp"))

    @property
    def user(self):
        return Capability(self._keyed_factory("user"))

    @property
    def video_clip(self):
        return Capability(self._keyed_factory("videoClip"), _INT_VIDEOCLIP)

    class Wifi(capabilities.Capabilities.Wifi):
        """WIFI"""

        __slots__ = ("_factory",)

        def __init__(self, factory: Callable[[], dict]) -> None:
            super().__init__()
            self._factory = factory

        def _keyed_factory(self, key: str):
            def _factory() -> dict:
                if (value := self._factory()) is None:
                    return None
                return value.get(key, None)

            return _factory

        @property
        def _value(self):
            return Capability(self._keyed_factory("wifi"))

        @property
        def value(self):
            return self._value.value

        @property
        def permissions(self):
            return self._value.permissions

        def __bool__(self):
            return bool(self.value)

        @property
        def testable(self):
            return Capability(self._keyed_factory("wifiTest"))

    @property
    def wifi(self):
        return type(self).Wifi(self._factory)

    def update(self, value: "Capabilities"):
        if not isinstance(value, type(self)):
            raise TypeError("Can only update from another Capabilities")
        # pylint: disable=protected-access
        self._value = value._value
        return self

    def __repr__(self):
        return f"<{self.__class__.__name__}: {repr(self._value)}>"
