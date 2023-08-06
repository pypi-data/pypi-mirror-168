"""REST PTZ Mixin"""

from async_reolink.api import ptz
from async_reolink.api.ptz.typings import (
    Patrol,
    Preset,
    ZoomOperation,
    Operation,
    Track,
)

from async_reolink.rest.ptz.models import MutablePatrol

from ..commands import ptz as commands


class PTZ(ptz.PTZ):
    """REST PTZ Mixin"""

    def _create_get_ptz_autofocus_request(self, channel: int):
        return commands.GetAutoFocusRequest(channel)

    def _create_set_ptz_autofocus_request(self, channel: int, disabled: bool):
        return commands.SetAutoFocusRequest(disabled, channel_id=channel)

    def _create_get_ptz_patrols_request(self, channel: int):
        return commands.GetPatrolRequest(channel)

    def _create_set_ptz_patrol_request(self, channel_id: int, patrol: Patrol):
        return commands.SetPatrolRequest(patrol, channel_id)

    def _create_get_ptz_presets_request(self, channel: int):
        return commands.GetPresetRequest(channel)

    def _create_set_ptz_preset_request(self, channel_id: int, preset: Preset):
        return commands.SetPresetRequest(preset, channel_id)

    def _create_get_ptz_tatterns_request(self, channel: int):
        return commands.GetTatternRequest(channel)

    def _create_set_ptz_tatterns_request(self, channel_id: int, *track: Track):
        return commands.SetTatternRequest(*track, channel_id=channel_id)

    def _create_get_ptz_zoom_focus_request(self, channel: int):
        return commands.GetZoomFocusRequest(channel)

    def _create_set_ptz_zoomfocus_request(
        self, channel: int, operation: ZoomOperation, position: int
    ):
        return commands.SetZoomFocusRequest(operation, position, channel)

    def _create_set_ptz_control_request(
        self,
        channel: int,
        operation: Operation,
        speed: int | None,
        preset_id: int | None,
    ):
        return commands.SetControlRequest(operation, speed, preset_id, channel)
