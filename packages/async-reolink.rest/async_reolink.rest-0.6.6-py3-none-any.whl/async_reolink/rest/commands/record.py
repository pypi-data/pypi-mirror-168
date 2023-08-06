"""REST Record Commands"""

from typing import Callable, Final, Sequence, TypeGuard, TypeVar
from async_reolink.api.commands import record
from async_reolink.api.record import typings

from ..record.models import MutableSearch, SearchStatus, File

from . import (
    _CHANNEL_KEY,
    CommandRequest,
    CommandRequestWithChannel,
    CommandResponse,
    CommandResponseTypes,
)

# pylint:disable=missing-function-docstring


class GetSnapshotRequest(CommandRequestWithChannel, record.GetSnapshotRequest):
    """REST Get Snaposhot Request"""

    COMMAND: Final = "Snap"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id

    @property
    def raw_parameter(self):
        return self._parameter


class SearchRecordingsRequest(CommandRequest, record.SearchRecordingsRequest):
    """REST Search Recordings Request"""

    COMMAND: Final = "Search"

    def __init__(
        self,
        search: typings.Search,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.search = search
        self.channel_id = channel_id

    def _get_search(self, create=False) -> dict:
        _key: Final = "Search"
        if (parameter := self._get_parameter(create)) is None:
            return None
        if _key in parameter or not create:
            return parameter.get(_key, None)
        return parameter.setdefault(_key, {})

    @property
    def _search(self):
        return self._get_search(True)

    @property
    def channel_id(self) -> int:
        if (value := self._get_search()) is None:
            return 0
        return value.get(_CHANNEL_KEY, 0)

    @channel_id.setter
    def channel_id(self, value):
        self._search[_CHANNEL_KEY] = value

    @property
    def search(self):
        return MutableSearch(self._get_search)

    @search.setter
    def search(self, value: typings.Search):
        if self._get_search() is None:
            if not isinstance(value, MutableSearch):
                value = MutableSearch(value)
            self._parameter["Search"] = value._factory(True)
        elif value is not None:
            search = self.search

            search.end = value.end
            search.start = value.start
            search.status_only = value.status_only
            search.stream_type = value.stream_type


_T = TypeVar("_T")


class _FactorySequence(Sequence[_T]):

    __slots__ = ("_factory", "_get_value")

    def __init__(
        self, getter: Callable[[], list], factory: Callable[[Callable[[], dict]], _T]
    ) -> None:
        super().__init__()
        self._get_value = getter
        self._factory = factory

    def _get_item(self, __k: int) -> dict:
        return value[__k] if (value := self._get_value()) is not None else None

    def __getitem__(self, __k: int):
        def _factory():
            return self._get_item(__k)

        return self._factory(_factory)

    def __len__(self):
        if (_list := self._get_value()) is None:
            return 0
        return len(_list)


class SearchRecordingsResponse(
    CommandResponse, record.SearchRecordingsResponse, test="is_response"
):
    """REST Search Results"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, SearchRecordingsRequest.COMMAND)

    def _get_sub_value(self) -> list:
        return (
            value.get("SearchResult", None)
            if (value := self._get_value()) is not None
            else None
        )

    @property
    def channel_id(self) -> int:
        if (value := self._get_sub_value()) is None:
            return 0
        return value.get(_CHANNEL_KEY, 0)

    def _get_status(self) -> list:
        return (
            value.get("Status", None)
            if (value := self._get_sub_value()) is not None
            else None
        )

    @property
    def status(self):
        return _FactorySequence(self._get_status, SearchStatus)

    def _get_file(self) -> list:
        return (
            value.get("File", None)
            if (value := self._get_sub_value()) is not None
            else None
        )

    @property
    def files(self):
        return _FactorySequence(self._get_file, File)
