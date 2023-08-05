"""REST LED Mixin"""

from typing import Mapping, Sequence
from async_reolink.api import led
from async_reolink.api.led.typings import LightStates, LightingSchedule, WhiteLedInfo
from async_reolink.api.ai.typings import AITypes
from async_reolink.api.typings import PercentValue

from ..commands import led as commands


class LED(led.LED):
    """REST LED Mixin"""

    def _create_get_ir_lights_request(self, channel: int):
        return commands.GetIrLightsRequest(channel)

    def _create_set_ir_lights_request(self, state: LightStates, channel: int):
        return commands.SetIrLightsRequest(state, channel)

    def _create_get_power_led_request(self, channel: int):
        return commands.GetPowerLedRequest(channel)

    def _create_set_power_led_request(self, state: LightStates, channel: int):
        return commands.SetPowerLedRequest(state, channel)

    def _create_get_white_led_request(self, channel: int):
        return commands.GetWhiteLedRequest(channel)

    def _create_set_white_led_request(
        self,
        info: WhiteLedInfo,
        channel: int,
    ):
        req = commands.SetWhiteLedRequest(channel)
        req.info.state = info.state
        if info.brightness is not None:
            req.info.brightness = info.brightness
        if info.brightness_state is not None:
            req.info.brightness_state = info.brightness_state
        if info.lighting_schedule is not None:
            req.info.lighting_schedule = info.lighting_schedule
        if info.ai_detection_type is not None:
            req.info.ai_detection_type = info.ai_detection_type
        return req
