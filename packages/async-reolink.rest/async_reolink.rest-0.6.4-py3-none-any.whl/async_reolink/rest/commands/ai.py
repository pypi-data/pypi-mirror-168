"""AI REST Commands"""

from typing import Final, TypeGuard

from async_reolink.api.commands import ai

# from async_reolink.api.ai import typings

from ..ai import models
from . import (
    _CHANNEL_KEY,
    CommandResponse,
    CommandResponseTypes,
    CommandRequestWithChannel,
    CommandResponseWithChannel,
)

# pylint:disable=missing-function-docstring


class GetAiStateRequest(CommandRequestWithChannel, ai.GetAiStateRequest):
    """Get AI State"""

    __slots__ = ()

    COMMAND: Final = "GetAiState"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


_NONE_DICT: Final[dict] = None


class GetAiStateResponse(
    CommandResponse,
    ai.GetAiStateResponse,
    test="is_response",
):
    """Get AI State Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetAiStateRequest.COMMAND)

    @property
    def channel_id(self) -> int:
        if (value := self._get_value()) is None:
            return None
        return value.get(_CHANNEL_KEY, None)

    @property
    def state(self):
        return models.State(self._get_value())


class GetAiConfigRequest(CommandRequestWithChannel, ai.GetAiConfigRequest):
    """Get AI Configuration"""

    COMMAND: Final = "GetAiCfg"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


class GetAiConfigResponse(
    CommandResponseWithChannel,
    ai.GetAiConfigResponse,
    test="is_response",
):
    """Get AI Configuration Response"""

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetAiConfigRequest.COMMAND)

    @property
    def channel_id(self) -> int:
        if (value := self._get_value()) is None:
            return None
        return value.get(_CHANNEL_KEY, None)

    @property
    def config(self):
        return models.Config(self._get_value())


class SetAiConfigRequest(CommandRequestWithChannel, ai.SetAiConfigRequest):
    """Set AI Configuration"""

    COMMAND: Final = "SetAiCfg"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id

    @property
    def config(self):
        return models.MutableConfig(self._get_parameter)
