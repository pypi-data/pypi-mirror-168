"""Encoding REST Commands"""

from typing import Final, TypeGuard
from async_reolink.api.commands import encoding

from ..encoding.models import EncodingInfo

from ..commands import (
    _CHANNEL_KEY,
    CommandResponseTypes,
    CommandRequestWithChannel,
    CommandResponse,
)

# pylint: disable=missing-function-docstring


class GetEncodingRequest(CommandRequestWithChannel, encoding.GetEncodingRequest):
    """Get Encoding REST Request"""

    COMMAND: Final = "GetEnc"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


class GetEncodingResponse(
    CommandResponse, encoding.GetEncodingResponse, test="is_response"
):
    """Get Encoding REST Response"""

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetEncodingRequest.COMMAND)

    def _get_info(self) -> dict:
        if (value := self._get_value()) is None:
            return None
        return value.get("Enc", None)

    @property
    def channel_id(self) -> int:
        if (info := self._get_info()) is not None:
            return info.get(_CHANNEL_KEY, 0)
        return 0

    @property
    def info(self):
        return EncodingInfo(self._get_info)
