"""Encoding REST models"""

from typing import Callable, Mapping
from async_reolink.api.typings import StreamTypes
from async_reolink.api.encoding import typings

from .typings import STREAMTYPES_STR_MAP

# pylint:disable=missing-function-docstring


class StreamEncodingInfo(typings.StreamEncodingInfo):
    """REST Stream Encoding Info"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        super().__init__()
        self._factory = factory

    @property
    def bit_rate(self) -> int:
        if (value := self._factory()) is not None:
            return value.get("bitRate", 0)
        return 0

    @property
    def frame_rate(self) -> int:
        if (value := self._factory()) is not None:
            return value.get("frameRate", 0)
        return 0

    @property
    def gop(self) -> int:
        if (value := self._factory()) is not None:
            return value.get("gop", 0)
        return 0

    @property
    def height(self) -> int:
        if (value := self._factory()) is not None:
            return value.get("height", 0)
        return 0

    @property
    def width(self) -> int:
        if (value := self._factory()) is not None:
            return value.get("width", 0)
        return 0

    @property
    def profile(self) -> int:
        if (value := self._factory()) is not None:
            return value.get("profile", "")
        return ""

    @property
    def size(self) -> int:
        if (value := self._factory()) is not None:
            return value.get("size", "")
        return ""

    @property
    def video_type(self) -> int:
        if (value := self._factory()) is not None:
            return value.get("video_type", "")
        return ""


class _StreamMapping(Mapping[StreamTypes, StreamEncodingInfo]):
    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        super().__init__()
        self._factory = factory

    def __getitem__(self, __k: StreamTypes):
        def _get():
            if (_dict := self._factory()) is not None:
                return _dict.get(STREAMTYPES_STR_MAP[__k], None)
            return None

        return StreamEncodingInfo(_get)

    def __iter__(self):
        if (_dict := self._factory()) is None:
            return
        for __k in StreamTypes:
            if STREAMTYPES_STR_MAP[__k] in _dict:
                yield __k

    def __len__(self):
        if (_dict := self._factory()) is None:
            return 0
        return len((__k for __k in StreamTypes if STREAMTYPES_STR_MAP[__k] in _dict))


class EncodingInfo(typings.EncodingInfo):
    """REST Encoding Info"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        super().__init__()
        self._factory = factory

    @property
    def audio(self) -> int:
        if (value := self._factory()) is not None:
            return value.get("audio", 0)
        return 0

    @property
    def stream(self):
        """stream"""

        return _StreamMapping(self._factory)
