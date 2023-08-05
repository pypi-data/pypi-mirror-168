""" ReoLink REST API """

from . import (
    ai,
    alarm,
    encoding,
    connection,
    led,
    ptz,
    network,
    system,
    record,
    security,
    video,
)

from .__version__ import __version__


class Client(
    connection.Connection,
    security.Security,
    system.System,
    network.Network,
    video.Video,
    encoding.Encoding,
    record.Record,
    alarm.Alarm,
    ai.AI,
    led.LED,
    ptz.PTZ,
):
    """Rest API Client"""

    def __init__(self, session_factory: connection.SessionFactory = None) -> None:
        super().__init__(session_factory=session_factory)


# __all__ = ["Client", "__version__"]
