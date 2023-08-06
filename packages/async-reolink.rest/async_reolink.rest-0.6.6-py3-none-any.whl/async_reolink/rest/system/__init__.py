"""System Mixin"""

from async_reolink.api import system

from ..commands import system as commands
from .capabilities import Capabilities


class System(system.System):
    """Rest System Mixin"""

    def _create_get_capabilities_request(self, username: str | None):
        return commands.GetAbilitiesRequest(
            username if username is not None else "null"
        )

    def _create_empty_capabilities(self):
        def _factory():
            return None

        return Capabilities(_factory)

    def _create_get_device_info_request(self):
        return commands.GetDeviceInfoRequest()

    def _create_empty_device_info(self):
        def _factory():
            return None

        return commands.DeviceInfo(_factory)

    def _create_get_time_request(self):
        return commands.GetTimeRequest()

    def _create_reboot_request(self):
        return commands.RebootRequest()

    def _create_get_hdd_info_request(self):
        return commands.GetHddInfoRequest()
