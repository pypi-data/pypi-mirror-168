"""REST LED Commands"""

from typing import Final, TypeGuard

from async_reolink.api.commands import led
from async_reolink.api.led import typings

from ..led.typings import LIGHTSTATES_STR_MAP, STR_LIGHTSTATES_MAP
from ..led.models import MutableWhiteLedInfo, WhiteLedInfo

from . import (
    _CHANNEL_KEY,
    CommandRequest,
    CommandRequestWithChannel,
    CommandResponseTypes,
    CommandResponse,
)

# pylint:disable=missing-function-docstring


class GetIrLightsRequest(CommandRequestWithChannel, led.GetIrLightsRequest):
    """REST Get IR Lights"""

    __slots__ = ()

    COMMAND: Final = "GetIrLights"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


_IR_LIGHTS_KEY = "IrLights"

_DEFAULT_LIGHTSTATE: Final = typings.LightStates.OFF
_DEFAULT_LIGHTSTATE_STR: Final = LIGHTSTATES_STR_MAP[_DEFAULT_LIGHTSTATE]


class GetIrLightsResponse(CommandResponse, led.GetIrLightsResponse, test="is_response"):
    """REST Get IR Lights Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetIrLightsRequest.COMMAND)

    def _get_lights(self) -> dict:
        return (
            value.get(_IR_LIGHTS_KEY, None)
            if (value := self._get_value()) is not None
            else None
        )

    @property
    def channel_id(self) -> int:
        return (
            value.get(_CHANNEL_KEY, 0)
            if (value := self._get_lights()) is not None
            else 0
        )

    @property
    def state(self) -> typings.LightStates:
        return (
            STR_LIGHTSTATES_MAP[value.get("state", _DEFAULT_LIGHTSTATE_STR)]
            if (value := self._get_lights()) is not None
            else _DEFAULT_LIGHTSTATE
        )


class SetIrLightsRequest(CommandRequest, led.SetIrLightsRequest):
    """REST Set Ir Lights"""

    __slots__ = ()

    COMMAND: Final = "SetIrLights"

    def __init__(
        self,
        state: typings.LightStates,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id
        self.state = state

    def _get_lights(self, create=False) -> dict:
        _key: Final = _IR_LIGHTS_KEY
        if (parameter := self._get_parameter(create)) is None:
            return None
        if _key in parameter or not create:
            return parameter.get(_key, None)
        return parameter.setdefault(_key, {})

    @property
    def _lights(self):
        return self._get_lights(True)

    @GetIrLightsResponse.channel_id.setter
    def channel_id(self, value):
        self._lights[_CHANNEL_KEY] = value

    @GetIrLightsResponse.state.setter
    def state(self, value):
        self._lights["state"] = LIGHTSTATES_STR_MAP[value]


class GetPowerLedRequest(CommandRequest, led.GetPowerLedRequest):
    """REST Get Power LED"""

    __slots__ = ()

    COMMAND: Final = "GetPowerLed"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__(self.COMMAND, response_type)
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


_POWER_LED_KEY = "PowerLed"


class GetPowerLedResponse(CommandResponse, led.GetPowerLedResponse, test="is_response"):
    """REST Get Power LED Response"""

    __slots__ = ()

    state = GetIrLightsResponse.state
    channel_id = GetIrLightsResponse.channel_id

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetPowerLedRequest.COMMAND)

    def _get_lights(self) -> dict:
        return (
            value.get(_POWER_LED_KEY, None)
            if (value := self._get_value()) is not None
            else None
        )


class SetPowerLedRequest(CommandRequest, led.SetPowerLedRequest):
    """REST Set Power LED"""

    __slots__ = ()

    COMMAND: Final = "SetPowerLed"

    def __init__(
        self,
        state: typings.LightStates,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__(self.COMMAND, response_type)
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id
        self.state = state

    def _get_lights(self, create=False) -> dict:
        _key: Final = _POWER_LED_KEY
        if (parameter := self._get_parameter(create)) is None:
            return None
        if _key in parameter or not create:
            return parameter.get(_key, None)
        return parameter.setdefault(_key, {})

    _lights = SetIrLightsRequest._lights
    channel_id = SetIrLightsRequest.channel_id
    state = SetIrLightsRequest.state


class GetWhiteLedRequest(CommandRequestWithChannel, led.GetWhiteLedRequest):
    """REST Get White LED"""

    __slots__ = ()

    COMMAND: Final = "GetWhiteLed"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__(self.COMMAND, response_type)
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


_WHITE_LED_KEY = "WhiteLed"


class GetWhiteLedResponse(CommandResponse, led.GetWhiteLedResponse, test="is_response"):
    """REST Get White LED Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetWhiteLedRequest.COMMAND)

    def _get_lights(self) -> dict:
        return (
            value.get(_WHITE_LED_KEY, None)
            if (value := self._get_value()) is not None
            else None
        )

    channel_id = GetIrLightsResponse.channel_id

    @property
    def info(self) -> WhiteLedInfo:
        return WhiteLedInfo(self._get_lights)


class SetWhiteLedRequest(CommandRequest, led.SetWhiteLedRequest):
    """REST Set White LED"""

    __slots__ = ()

    COMMAND: Final = "SetWhiteLed"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__(self.COMMAND, response_type)
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id

    def _get_lights(self, create=False) -> dict:
        _key: Final = _WHITE_LED_KEY
        if (parameter := self._get_parameter(create)) is None:
            return None
        if _key in parameter or not create:
            return parameter.get(_key, None)
        return parameter.setdefault(_key, {})

    @property
    def _info(self):
        return self._parameter.setdefault(_WHITE_LED_KEY, {})

    _lights = _info

    channel_id = SetIrLightsRequest.channel_id

    @property
    def info(self):
        return MutableWhiteLedInfo(self._get_lights)
