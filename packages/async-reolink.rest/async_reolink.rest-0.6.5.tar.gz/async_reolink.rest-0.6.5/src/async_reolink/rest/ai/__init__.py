"""AI Mixin"""

from typing import Mapping

from async_reolink.api import ai
from async_reolink.api.ai.typings import AITypes

from ..commands import ai as commands


class AI(ai.AI):
    """Rest AI Mixin"""

    def _create_get_ai_state_request(self, channel: int):
        return commands.GetAiStateRequest(channel)

    def _create_get_ai_config_request(self, channel: int):
        return commands.GetAiStateRequest(channel)

    def _create_set_ai_config(
        self,
        channel: int,
        detect: AITypes | set[AITypes] | Mapping[AITypes, bool] | None,
        track: AITypes | set[AITypes] | Mapping[AITypes, bool] | None,
    ):
        return commands.SetAiConfigRequest(channel, detect, track)
