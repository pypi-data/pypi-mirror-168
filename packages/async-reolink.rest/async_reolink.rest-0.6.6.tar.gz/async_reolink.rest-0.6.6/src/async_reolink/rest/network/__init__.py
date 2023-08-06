"""REST Network Mixin"""

from async_reolink.api import network
from async_reolink.api.typings import StreamTypes

from ..commands import network as commands

from .. import security


class Network(network.Network):
    """REST Network Mixin"""

    def _create_get_channel_status_request(self):
        return commands.GetChannelStatusRequest()

    def _create_get_local_link_request(self):
        return commands.GetLocalLinkRequest()

    def _create_get_p2p_request(self):
        return commands.GetP2PRequest()

    def _create_get_ports_request(self):
        return commands.GetNetworkPortsRequest()

    def _create_get_rtsp_urls_request(self, channel_id: int = 0):
        return commands.GetRTSPUrlsRequest(channel_id)

    async def get_rtmp_url(self, channel: int = 0, stream: StreamTypes = ...):
        url = await super().get_rtmp_url(channel, stream)
        if isinstance(self, security.Security):
            token = self._auth_token
            if token is not None:
                url += f"&token={token}"
        return url

    def _create_get_wifi_info_request(self):
        return commands.GetWifiInfoRequest()

    def _create_get_wifi_signal_request(self):
        return commands.GetWifiSignalRequest()
