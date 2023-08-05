"""Secuirty REST Commands"""

from typing import Final, TypeGuard
from async_reolink.api.commands import security

from . import CommandRequest, CommandResponseTypes, CommandResponse

from ..security.models import LoginToken

# pylint:disable=missing-function-docstring


class LoginRequest(CommandRequest, security.LoginRequest):
    """REST Login Request"""

    __slots__ = ()

    COMMAND: Final = "Login"

    def __init__(
        self,
        user_name: str,
        password: str,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.user_name = user_name
        self.password = password

    def _get_login(self, create=False) -> dict:
        _key: Final = "User"
        if (parameter := self._get_parameter(create)) is None:
            return None
        if _key in parameter or not create:
            return parameter.get(_key, None)
        return parameter.setdefault(_key, {})

    @property
    def _login(self):
        return self._get_login(True)

    @property
    def user_name(self) -> str:
        return (
            value.get("userName", "")
            if (value := self._get_login()) is not None
            else ""
        )

    @user_name.setter
    def user_name(self, value):
        self._login["userName"] = value

    @property
    def password(self) -> str:
        return (
            value.get("password", "")
            if (value := self._get_login()) is not None
            else ""
        )

    @password.setter
    def password(self, value):
        self._login["password"] = value


class LoginResponse(CommandResponse, security.LoginResponse, test="is_response"):
    """REST Login Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, LoginRequest.COMMAND)

    def _get_token(self) -> dict:
        return (
            value.get("Token", None)
            if (value := self._get_value()) is not None
            else None
        )

    @property
    def token(self):
        return LoginToken(self._get_token)


class LogoutRequest(CommandRequest, security.LogoutRequest):
    """REST Logut Request"""

    __slots__ = ()

    COMMAND: Final = "Logout"

    def __init__(
        self, response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
