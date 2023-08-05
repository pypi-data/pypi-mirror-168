"""REST Connection"""
from __future__ import annotations

from enum import IntEnum
import inspect
from json import JSONDecoder, loads as DEFAULT_JSON_DECODER
import logging
from typing import (
    TYPE_CHECKING,
    Callable,
    Protocol,
    Sequence,
    cast,
    overload,
)
from urllib.parse import urlparse
import aiohttp

from async_reolink.api.commands import (
    CommandResponse as BaseCommandResponse,
    CommandRequest as BaseCommandRequest,
)
from async_reolink.api.connection import Connection as BaseConnection

from async_reolink.api import errors

from async_reolink.api.const import DEFAULT_TIMEOUT

from .commands import CommandResponse, CommandRequest

from .errors import CONNECTION_ERRORS, RESPONSE_ERRORS

_LOGGER = logging.getLogger(__name__)
_LOGGER_DATA = logging.getLogger(__name__ + ".data")


class SessionFactory(Protocol):
    """Session Factory"""

    def __call__(self, base_url: str, timeout: int) -> aiohttp.ClientSession:
        ...


def _default_create_session(base_url: str, timeout: int):
    return aiohttp.ClientSession(
        base_url=base_url,
        timeout=aiohttp.ClientTimeout(total=timeout),
        connector=aiohttp.TCPConnector(ssl=False),
    )


class Encryption(IntEnum):
    """Connection Encryption"""

    NONE = 0
    HTTPS = 1


class Connection(BaseConnection):
    """REST Connection"""

    def __init__(
        self,
        *args,
        session_factory: SessionFactory = None,
        loads: JSONDecoder = DEFAULT_JSON_DECODER,
        **kwargs,
    ):
        self._force_get_callbacks: list[
            Callable[[str, dict[str, str], Sequence[CommandRequest]], any]
        ] = []
        # self._response_callback: list[Callable[[CommandResponse], None]]
        super().__init__(*args, **kwargs)
        self.__session: aiohttp.ClientSession | None = None
        self.__session_factory: SessionFactory = (
            session_factory or _default_create_session
        )
        self.__base_url = ""
        self.__hostname = ""
        self.__connection_id = 0
        self.__loads = loads

    def _create_session(self, timeout: int):
        return self.__session_factory(self.__base_url, timeout)

    @property
    def is_connected(self):
        """is connected"""
        return self.__connection_id != 0

    @property
    def connection_id(self):
        """connection id"""
        return self.__connection_id

    @property
    def base_url(self):
        """base url"""
        return self.__base_url

    @property
    def secured(self):
        """Secure connection"""
        return self.__base_url.startswith("https:")

    @property
    def hostname(self):
        """hostname"""
        return self.__hostname

    @overload
    async def connect(
        self,
        hostname: str,
        port: int = None,
        timeout: float = DEFAULT_TIMEOUT,
        *,
        encryption: Encryption = Encryption.NONE,
    ):  # pylint: disable=arguments-differ
        ...

    async def connect(
        self,
        hostname: str,
        port: int = None,
        timeout: float = DEFAULT_TIMEOUT,
        **kwargs,
    ):
        """setup connection to device"""
        encryption = kwargs.get("encryption", Encryption.NONE)
        if port == 443 or (port is None and encryption == Encryption.HTTPS):
            https = True
            port = None
        elif port == 80 and encryption != Encryption.HTTPS:
            https = False
            port = None
        else:
            https = encryption == Encryption.HTTPS

        scheme = "https" if https is True else "http"
        _port = f":{port}" if port is not None else ""
        url = f"{scheme}://{hostname}{_port}"
        _id = hash(url)
        if _id == self.__connection_id:
            return
        if self.__connection_id != 0:
            await self.disconnect()

        self.__base_url = url
        self.__connection_id = _id
        self.__hostname = hostname
        self.__session = self._create_session(timeout)

        for callback in self._connect_callbacks:
            if inspect.iscoroutinefunction(callback):
                await callback()
            else:
                callback()

    async def disconnect(self):
        """disconnect from device"""

        if self.__session is None:
            return
        for callback in self._disconnect_callbacks:
            if inspect.iscoroutinefunction(callback):
                await callback()
            else:
                callback()
        if not self.__session.closed:
            await self.__session.close()
        self.__connection_id = 0
        self.__base_url = ""
        self.__hostname = ""
        self.__session = None

    def __process_response(self, value: any):
        if not CommandResponse.is_response(value):
            raise errors.ReolinkResponseError("Invalid response from device")
        response = CommandResponse.create_from(value)
        # for handler in self._response_callback:
        #    handler(response)
        return response

    async def __execute(self, *args: CommandRequest):
        if not self.is_connected:
            return

        if len(args) == 0:
            return
        use_get = False
        query = {}
        url = "/cgi-bin/api.cgi"
        for callback in self._force_get_callbacks:
            if inspect.iscoroutinefunction(callback):
                cb_result = await callback(url, query, args)
            else:
                cb_result = callback(url, query, args)

            if cb_result:
                if isinstance(cb_result, tuple) and len(cb_result) == 2:
                    if not use_get:
                        use_get = bool(cb_result[0])
                    url = str(cb_result[1])
                elif isinstance(cb_result, str):
                    url = cb_result
                elif not use_get:
                    use_get = True

        count = None

        headers = {"Accept": "*/*", "Content-Type": "application/json"}

        cleanup = True
        response = None
        context = None

        def _cleanup():
            nonlocal response, context
            if response:
                response.close()
            response = None
            if context:
                context.close()
            context = None

        try:
            encrypted = False
            if use_get:
                _LOGGER_DATA.debug("GET: %s<-%s", url, query)
                context = self.__session.get(
                    url,
                    params=query,
                    headers=headers,
                    allow_redirects=False,
                )
            else:
                data = self.__session.json_serialize(
                    list(map(lambda r: r._get_request(), args))
                )

                _LOGGER_DATA.debug(
                    "%s%s<-%s", self.__hostname, "(E)" if encrypted else "", data
                )
                context = self.__session.post(
                    url,
                    data=data,
                    headers=headers,
                    allow_redirects=False,
                )

            response = await context
            if count is not None:
                count.free = True
            if response.status in (302, 301) and "location" in response.headers:
                location = response.headers["location"]
                redir = urlparse(location)
                base = urlparse(self.__base_url)
                if (
                    base.scheme != redir.scheme
                    and base.scheme == "http"
                    or redir.scheme == "http"
                ):
                    if redir.scheme == "http":
                        _LOGGER.warning(
                            "Got http redirect from camera (%s), please verify configuration",
                            self.__base_url,
                        )
                        await self.connect(
                            redir.hostname,
                            redir.port,
                            self.__session.timeout.total,
                            encryption=Encryption.NONE,
                        )
                    else:
                        _LOGGER.warning(
                            "Got https redirect from camera (%s), please verify configuration",
                            self.__base_url,
                        )
                        await self.connect(
                            redir.hostname,
                            redir.port,
                            self.__session.timeout.total,
                            encryption=Encryption.HTTPS,
                        )
                    async for command_response in self.__execute(*args):
                        if TYPE_CHECKING:
                            command_response = cast(
                                bytes | BaseCommandResponse, command_response
                            )
                        yield command_response
                    return

                _LOGGER.error(
                    "got unexpected redirect from camera (%s), please verify configurtation",
                    self.__base_url,
                )
                raise aiohttp.ClientResponseError(
                    response.request_info,
                    [response],
                    status=response.status,
                    headers=response.headers,
                )

            if response.status >= 500:
                _LOGGER.error("got critical (%d) response code", response.status)
                raise aiohttp.ClientResponseError(
                    response.request_info,
                    [response],
                    status=response.status,
                    headers=response.headers,
                )
            if response.status >= 400:
                _LOGGER.error("got auth (%d) response code", response.status)
                raise aiohttp.ClientResponseError(
                    response.request_info,
                    [response],
                    status=response.status,
                    headers=response.headers,
                )

            cleanup = False
        except CONNECTION_ERRORS:
            raise
        except RESPONSE_ERRORS:
            raise
        except Exception as unhandled_error:
            _LOGGER.error("unhandled exception")
            raise errors.ReolinkUnhandledError() from unhandled_error
        finally:
            if cleanup:
                _cleanup()

        if not response:
            return

        if "json" in response.content_type:
            try:
                command_responses = await response.json()
            finally:
                _cleanup()
        elif "text" in response.content_type:
            try:
                command_responses = await response.text()
            finally:
                _cleanup()

            if command_responses[0] != "[":
                _LOGGER.error("did not get json as response: (%s)", data)
                raise errors.ReolinkResponseError(
                    code=errors.ErrorCodes.PROTOCOL_ERROR,
                    details="invalid response",
                )

            command_responses = self.__loads(command_responses)
        else:
            try:
                async for chunk in response.content.iter_any():
                    yield chunk
            finally:
                _cleanup()
            return

        if not isinstance(command_responses, list):
            yield self.__process_response(command_responses)
            return

        _LOGGER_DATA.debug(
            "%s%s->%s", self.__hostname, "(D)" if encrypted else "", command_responses
        )

        for command_response in command_responses:
            yield self.__process_response(command_response)

    def _execute(self, *args: BaseCommandRequest):
        """Internal API"""

        return self.__execute(*args)
