"""REST Network Models"""

from typing import Callable, Final, Mapping
from async_reolink.api.network import typings

from .typings import STR_LINKTYPES_MAP

# pylint: disable=missing-function-docstring


class IPInfo(typings.IPInfo):
    """REST IP Info"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    @property
    def gateway(self) -> str:
        if (value := self._factory()) is None:
            return None
        return value.get("gateway", None)

    @property
    def address(self) -> str:
        if (value := self._factory()) is None:
            return None
        return value.get("ip", None)

    @property
    def mask(self) -> str:
        if (value := self._factory()) is None:
            return None
        return value.get("mask", None)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {repr(self._factory())}>"


class DNSInfo(typings.DNSInfo):
    """REST DNS Info"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    @property
    def auto(self) -> bool:
        if (value := self._factory()) is None:
            return 0
        return value.get("auto", 0)

    @property
    def dns_1(self) -> bool:
        if (value := self._factory()) is None:
            return None
        return value.get("dns1", None)

    @property
    def dns_2(self) -> bool:
        if (value := self._factory()) is None:
            return None
        return value.get("dns2", None)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {repr(self._factory())}>"


class LinkInfo(typings.LinkInfo):
    """REST Link Info"""

    __slots__ = ("_value",)

    def __init__(self, value: dict) -> None:
        if value is None:
            value = {}
        self._value = value

    @property
    def active_link(self) -> str:
        return self._value.get("activeLink", None)

    @property
    def mac(self) -> str:
        return self._value.get("mac", None)

    @property
    def type(self):
        if (value := self._value.get("type", None)) is None:
            return None
        return STR_LINKTYPES_MAP[value]

    @property
    def ip(self):  # pylint: disable=invalid-name
        def _get():
            return self._value.get("static", None)

        return IPInfo(_get)

    @property
    def dns(self):
        def _get():
            return self._value.get("dns", None)

        return DNSInfo(_get)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {repr(self._value)}>"


_CHANNEL_KEY: Final = "channel"


class ChannelStatus(typings.ChannelStatus):
    """REST Channel Status"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    @property
    def channel_id(self) -> int:
        if (value := self._factory()) is None:
            return None
        return value.get(_CHANNEL_KEY, None)

    @property
    def name(self) -> str:
        if (value := self._factory()) is None:
            return ""
        return value.get("name", "")

    @property
    def online(self) -> bool:
        if (value := self._factory()) is None:
            return 0
        return value.get("online", 0)

    @property
    def type(self) -> str:
        if (value := self._factory()) is None:
            return None
        return value.get("typeInfo", None)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {repr(self._factory())}>"


class ChannelStatuses(Mapping[int, ChannelStatus]):
    """Channel Statuses"""

    __slots__ = ("_value",)

    def __init__(self, value: dict) -> None:
        super().__init__()
        if value is None:
            value = {}
        self._value = value

    def _factory(self):
        return self._value

    @staticmethod
    def _get_channel(value: dict) -> int:
        return value.get(_CHANNEL_KEY, None) if value is not None else None

    def _get_channels(self) -> list:
        return self._value.get("status", None)

    def _channel_getter(self, channel_id: int):
        def _is_channel(value: dict):
            return type(self)._get_channel(value) == channel_id

        def _factory() -> dict:
            if (channels := self._get_channels()) is None:
                return None
            return next(filter(_is_channel, channels), None)

        return _factory

    def __getitem__(self, __k: int):
        return ChannelStatus(self._channel_getter(__k))

    def __iter__(self):
        if (channels := self._get_channels()) is None:
            return
        for _d in channels:
            if (channel := type(self)._get_channel(_d)) is not None:
                yield channel

    def __contains__(self, __o: int) -> bool:
        return self._channel_getter(__o)() is not None

    def __len__(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("count", 0)

    def update(self, value: "ChannelStatuses"):
        if not isinstance(value, type(self)):
            raise TypeError("Can only update from another ChannelStatuses")
        # pylint: disable=protected-access
        self._value = value._value
        return self

    def __repr__(self):
        return f"<{self.__class__.__name__}: {repr(self._value)}>"


class P2PInfo(typings.P2PInfo):
    """REST P2P Info"""

    __slots__ = ("_value",)

    def __init__(self, value: dict) -> None:
        if value is None:
            value = {}
        self._value = value

    @property
    def enabled(self) -> bool:
        return self._value.get("enable", 0)

    @property
    def uid(self) -> str:
        return self._value.get("uid", None)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {repr(self._value)}>"


class NetworkPort(typings.NetworkPort):
    """REST Network Port"""

    __slots__ = ("_factory", "_prefix")

    def __init__(self, prefix: str, factory: Callable[[], dict]) -> None:
        self._prefix = prefix
        self._factory = factory

    @property
    def value(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get(self._prefix + "Port", 0)

    @property
    def enabled(self) -> bool:
        if (value := self._factory()) is None:
            return 0
        # some versions dont support Enable so the port cannot be disabled, so we default to true if Port exists
        return value.get(
            self._prefix + "Enable", 1 if self._prefix + "Port" in value else 0
        )

    def __bool__(self):
        return bool(self.enabled and self.value)

    def __int__(self):
        return self.value if self.enabled else 0

    def __str__(self):
        return str(self.value) if self.enabled else ""

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: enabled={bool(self.enabled)}, value={self.value}>"


class NetworkPorts(typings.NetworkPorts):
    """REST Network Ports"""

    __slots__ = ("_value",)

    def __init__(self, value: dict) -> None:
        if value is None:
            value = {}
        self._value = value

    def _factory(self):
        return self._value

    @property
    def media(self):
        return NetworkPort("media", self._factory)

    @property
    def http(self):
        return NetworkPort("http", self._factory)

    @property
    def https(self):
        return NetworkPort("https", self._factory)

    @property
    def onvif(self):
        return NetworkPort("onvif", self._factory)

    @property
    def rtsp(self):
        return NetworkPort("rtsp", self._factory)

    @property
    def rtmp(self):
        return NetworkPort("rtmp", self._factory)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {repr(self._factory())}>"


class WifiInfo(typings.WifiInfo):
    """REST Wifi Info"""

    __slots__ = ("_value",)

    def __init__(self, value: dict) -> None:
        self._value = value

    def _factory(self):
        return self._value

    @property
    def ssid(self) -> str:
        if (value := self._factory()) is None:
            return None
        return value.get("ssid", None)

    @property
    def password(self) -> str:
        if (value := self._factory()) is None:
            return None
        return value.get("password", None)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {repr(self._factory())}>"
