"""System REST Commands"""

from typing import Final
from async_reolink.api.commands import system

from .._utilities.dictlist import DictList

from ..system.models import DaylightSavingsTimeInfo, DeviceInfo, TimeInfo, StorageInfo

from ..commands import (
    CommandRequest,
    CommandResponseTypes,
    CommandResponse,
)

from ..system.capabilities import Capabilities

# pylint:disable=missing-function-docstring
# pylint: disable=too-few-public-methods


class GetAbilitiesRequest(CommandRequest, system.GetAbilitiesRequest):
    """REST Get Capabilities Request"""

    __slots__ = ()

    COMMAND: Final = "GetAbility"

    def __init__(
        self,
        username: str,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.user_name = username

    def _get_user(self, create=False) -> dict:
        _key: Final = "User"
        if (parameter := self._get_parameter(create)) is None:
            return None
        if _key in parameter or not create:
            return parameter.get(_key, None)
        return parameter.setdefault(_key, {})

    @property
    def _user(self) -> dict:
        return self._get_user(True)

    @property
    def user_name(self) -> str:
        return (
            value.get("userName", "") if (value := self._get_user()) is not None else ""
        )

    @user_name.setter
    def user_name(self, value):
        self._user["userName"] = value


class GetAbilitiesResponse(
    CommandResponse, system.GetAbilitiesResponse, test="is_response"
):
    """REST Get Capability Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetAbilitiesRequest.COMMAND)

    def _get_ability(self) -> dict:
        return (
            value.get("Ability", None)
            if (value := self._get_value()) is not None
            else None
        )

    @property
    def capabilities(self):
        # we are not passing the factory here since this object is meant to be updatable
        return Capabilities(self._get_ability())


class GetDeviceInfoRequest(CommandRequest, system.GetDeviceInfoRequest):
    """REST Get Device Info Request"""

    COMMAND: Final = "GetDevInfo"

    def __init__(
        self, response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetDeviceInfoResponse(
    CommandResponse, system.GetDeviceInfoResponse, test="is_response"
):
    """REST Get Device Info Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetDeviceInfoRequest.COMMAND)

    def _get_info(self) -> dict:
        return (
            value.get("DevInfo", None)
            if (value := self._get_value()) is not None
            else None
        )

    @property
    def info(self):
        """device info"""
        # we are not passing the factory here since this object is meant to be updatable
        return DeviceInfo(self._get_info())


class GetTimeRequest(CommandRequest, system.GetTimeRequest):
    """REST Get Time Request"""

    COMMAND: Final = "GetTime"

    def __init__(
        self, response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetTimeResponse(CommandResponse, system.GetTimeResponse, test="is_response"):
    """REST Get Time Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetTimeRequest.COMMAND)

    def _get_dst(self) -> dict:
        return (
            value.get("Dst", None) if (value := self._get_value()) is not None else None
        )

    @property
    def dst(self):
        return DaylightSavingsTimeInfo(self._get_dst)

    def _get_time(self) -> dict:
        return (
            value.get("Time", None)
            if (value := self._get_value()) is not None
            else None
        )

    @property
    def time(self):
        return TimeInfo(self._get_time)


class RebootRequest(CommandRequest, system.RebootRequest):
    """REST Reboot Request"""

    __slots__ = ()

    COMMAND: Final = "Reboot"

    def __init__(
        self, response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetHddInfoRequest(CommandRequest, system.GetHddInfoRequest):
    """REST Get HDD Info Request"""

    __slots__ = ()

    COMMAND: Final = "GetHddInfo"

    def __init__(
        self, response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetGddInfoResponse(
    CommandResponse, system.GetHddInfoResponse, test="is_response"
):
    """REST Get HDD Info Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetHddInfoRequest.COMMAND)

    def _get_info(self) -> list:
        return (
            value.get("HddInfo", None)
            if (value := self._get_value()) is not None
            else None
        )

    @property
    def info(self):
        return DictList("number", self._get_info(), StorageInfo)
