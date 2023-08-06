"""REST Commands"""

from abc import ABC
from enum import IntEnum
from json import dumps
from typing import (
    Callable,
    Final,
    TypeGuard,
)

from async_reolink.api import commands

_COMMAND_KEY: Final = "cmd"
_ACTION_KEY: Final = "action"

# pylint: disable=missing-function-docstring


class CommandResponseTypes(IntEnum):
    """Command Response Types"""

    VALUE_ONLY = 0
    DETAILED = 1


class CommandRequest(commands.CommandRequest):
    """Rest Command Request"""

    __slots__ = ("_request",)

    def __init__(self):
        self._request = {}

    def _get_request(self):
        return self._request

    def _get_parameter(self, create=False) -> dict:
        _key: Final = "param"

        if _key in self._request or not create:
            return self._request.get(_key, None)
        return self._request.setdefault(_key, {})

    @property
    def _parameter(self):
        return self._get_parameter(True)

    @property
    def command(self) -> str:
        return self._request.get(_COMMAND_KEY, "")

    @command.setter
    def command(self, value):
        self._request[_COMMAND_KEY] = value

    @property
    def response_type(self) -> CommandResponseTypes:
        return self._request.get(_ACTION_KEY, CommandResponseTypes.VALUE_ONLY)

    @response_type.setter
    def response_type(self, value):
        self._request[_ACTION_KEY] = value


_CHANNEL_KEY: Final = "channel"


class CommandRequestWithChannel(CommandRequest, commands.ChannelValue):
    """Rest Command Request with Channel Parameter"""

    __slots__ = ()

    @property
    def channel_id(self):
        return (
            parameter.get(_CHANNEL_KEY, 0)
            if (parameter := self._get_parameter()) is not None
            else 0
        )

    @channel_id.setter
    def channel_id(self, value):
        self._parameter[_CHANNEL_KEY] = value


_VALUE_KEY: Final = "value"
_CODE_KEY: Final = "code"
_ERROR_KEY: Final = "error"


class CommandResponse(commands.CommandResponse, ABC):
    """Rest Command Response"""

    _response_handlers: dict[type["CommandResponse"], Callable[[dict], bool]] = {}

    def __init_subclass__(  # pylint: disable=arguments-differ
        cls, test: str = None, **kwargs
    ) -> None:
        super().__init_subclass__(**kwargs)
        if (
            isinstance(test, str)
            and (call := getattr(cls, test, None)) is not None
            and callable(call)
        ):
            cls._response_handlers[cls] = call

    @classmethod
    def create_from(cls, value: dict):
        """wrap response in CommandResponse Implementation"""

        for (_type, test) in cls._response_handlers.items():
            if test(value):
                return _type(value)

        return CommandResponse(value)

    @classmethod
    def is_response(cls, value: any, /, command: str | None = None) -> TypeGuard[dict]:
        """value is command response json"""
        return (
            isinstance(value, dict)
            and _COMMAND_KEY in value
            and _CODE_KEY in value
            and (command is None or command == value[_COMMAND_KEY])
        )

    @classmethod
    def is_value(cls, response: dict):
        """response is a command value response"""
        return _VALUE_KEY in response and isinstance(response[_VALUE_KEY], dict)

    __slots__ = ("_response",)

    def __init__(self, response: dict) -> None:
        self._response = response

    def _underlying_value(self):
        return self._response

    @property
    def is_detailed(self):
        return self._get_initial() is not None or self._get_range() is not None

    @property
    def command(self) -> str:
        return self._response.get(_COMMAND_KEY, "")

    @property
    def code(self) -> int:
        return self._response.get(_CODE_KEY, 0)

    def _get_value(self) -> dict:
        return self._response.get(_VALUE_KEY, None)

    def _get_initial(self) -> dict:
        return self._response.get("initial", None)

    def _get_range(self) -> dict:
        return self._response.get("range", None)

    def _get_error(self) -> dict:
        return self._response.get(_ERROR_KEY, None)


class UnhandledCommandResponse(CommandResponse):
    """Unhandled/Unknown REST Command Response"""

    __slots__ = ()


_RSP_CODE_KEY: Final = "rspCode"


class CommandResponseWithCode(
    CommandResponse, commands.ResponseCode, test="is_response"
):
    """REST Command Response with code"""

    @classmethod
    def is_response(  # pylint: disable=signature-differs
        cls, value: any, /
    ) -> TypeGuard["CommandResponseWithCode"]:
        return (
            super().is_response(value)
            and super().is_value(value)
            and _RSP_CODE_KEY in value[_VALUE_KEY]
        )

    __slots__ = ()

    @property
    def response_code(self):
        return (
            value.get(_RSP_CODE_KEY, 0)
            if (value := self._get_value()) is not None
            else 0
        )


class CommandResponseWithChannel(CommandResponse, commands.ChannelValue):
    """Rest Command Response Value with Channel"""

    __slots__ = ()

    @property
    def channel_id(self):
        return (
            value.get(_CHANNEL_KEY, 0)
            if (value := self._get_value()) is not None
            else 0
        )


class CommandErrorResponse(
    CommandResponse, commands.CommandErrorResponse, test="is_error"
):
    """Rest Command Error Response"""

    __slots__ = ()

    @classmethod
    def is_error(cls, response: dict):
        """response is a command error response"""
        return _ERROR_KEY in response and isinstance(response[_ERROR_KEY], dict)

    @property
    def error_code(self) -> int:
        return (
            value.get(_RSP_CODE_KEY, 0)
            if (value := self._get_error()) is not None
            else 0
        )

    @property
    def details(self) -> str | None:
        return value.get("detail", 0) if (value := self._get_error()) is not None else 0
