"""REST Alarm Mixin"""

from async_reolink.api.alarm import Alarm as BaseAlarm

from ..commands import alarm


class Alarm(BaseAlarm):
    """REST Alarm Mixin"""

    def _create_get_md_state(self, channel: int):
        return alarm.GetMotionStateRequest(channel)
