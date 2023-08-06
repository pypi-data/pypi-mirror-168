"""REST Record"""

from datetime import datetime
from typing import Sequence
from async_reolink.api.typings import StreamTypes
from async_reolink.api.commands import (
    CommandRequest,
)
from async_reolink.api.record import Record as BaseRecord, typings

from async_reolink.rest.record.models import MutableSearch

from ..commands import _COMMAND_KEY, record
from .seed import Seed


from .. import connection


class Record(BaseRecord):
    """REST Record Mixin"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if isinstance(self, connection.Connection):
            self._force_get_callbacks.append(self.__force_get_login)

    def __force_get_login(
        self, _: str, query: dict[str, str], commands: Sequence[CommandRequest]
    ):
        command = commands[0]
        if len(commands) > 1 or not isinstance(command, record.GetSnapshotRequest):
            return
        query[_COMMAND_KEY] = command.command
        query.update(command.raw_parameter)
        query["rs"] = str(Seed())
        return True

    def _create_get_snapshot_request(self, channel: int):
        return record.GetSnapshotRequest(channel)

    def _create_search_request(self, channel: int, search: typings.Search):
        return record.SearchRecordingsRequest(channel, search)

    def _create_search(
        self,
        start_time: datetime,
        end_time: datetime,
        only_status: bool,
        stream_type: StreamTypes,
    ):
        search = MutableSearch()
        search.start = start_time
        search.end = end_time
        search.status_only = only_status
        search.stream_type = stream_type
        return search
