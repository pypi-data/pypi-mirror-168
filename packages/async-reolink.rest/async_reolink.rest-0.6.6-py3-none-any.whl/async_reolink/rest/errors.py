"""REST common errors"""

from typing import Final

from asyncio import TimeoutError as AsyncIOTimeoutError
from aiohttp import ClientConnectionError, ClientResponseError

from async_reolink.api.errors import ErrorCodes

CONNECTION_ERRORS: Final = (
    TimeoutError,
    AsyncIOTimeoutError,
    ClientConnectionError,
    ConnectionRefusedError
)

RESPONSE_ERRORS: Final = (
    ClientResponseError
)

AUTH_ERRORCODES: Final = (
    ErrorCodes.AUTH_REQUIRED,
    ErrorCodes.LOGIN_FAILED,
    ErrorCodes.PASSWORD_WRONG
)
