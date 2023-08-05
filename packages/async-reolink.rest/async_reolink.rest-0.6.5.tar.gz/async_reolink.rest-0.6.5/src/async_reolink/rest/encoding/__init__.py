"""AI Mixin"""

from async_reolink.api import encoding

from ..commands import encoding as commands


class Encoding(encoding.Encoding):
    """Rest Encoding Mixin"""

    def _create_get_encoding_request(self, channel: int):
        return commands.GetEncodingRequest(channel)
