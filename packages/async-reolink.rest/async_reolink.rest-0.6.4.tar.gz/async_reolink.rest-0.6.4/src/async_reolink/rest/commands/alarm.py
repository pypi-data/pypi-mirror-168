"""REST Alarm Commands"""

from typing import Final, TypeGuard
from async_reolink.api.commands import alarm

from . import CommandRequestWithChannel, CommandResponse, CommandResponseTypes


class GetMotionStateRequest(CommandRequestWithChannel, alarm.GetMotionStateRequest):
    """REST Get Motion State Request"""

    COMMAND: Final = "GetMdState"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


class GetMotionStateResponse(
    CommandResponse, alarm.GetMostionStateResponse, test="is_response"
):
    """REST Get Motion State Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetMotionStateRequest.COMMAND)

    @property
    def state(self) -> bool:
        return value.get("state", 0) if (value := self._get_value()) is not None else 0
