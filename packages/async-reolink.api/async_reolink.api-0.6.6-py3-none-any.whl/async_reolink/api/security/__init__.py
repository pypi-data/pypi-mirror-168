"""Security"""

from abc import ABC, abstractmethod
import inspect
from time import time
from typing import Callable


from ..const import DEFAULT_PASSWORD, DEFAULT_USERNAME

from ..commands import (
    CommandErrorResponse,
    ResponseCode,
)

from ..errors import ErrorCodes, ReolinkResponseError

from ..commands.security import (
    LoginRequest,
    LoginResponse,
    LogoutRequest,
    GetUserRequest,
    GetUserResponse,
)

from .. import connection


class Security(ABC):
    """Abstract Security Mixin"""

    def __init__(self, *args, **kwargs) -> None:
        self._logout_callbacks: list[Callable[[], None]] = []
        super().__init__(*args, **kwargs)
        if isinstance(self, connection.Connection):
            self._disconnect_callbacks.append(self.logout)

    @property
    @abstractmethod
    def is_authenticated(self) -> bool:
        """authentication status"""

    @property
    @abstractmethod
    def authentication_timeout(self) -> float:
        """authentication time remaining"""

    @property
    @abstractmethod
    def authentication_id(self) -> int:
        """authentication id"""

    @abstractmethod
    async def _prelogin(self, username: str) -> bool:
        ...

    @abstractmethod
    async def _process_login(self, response: LoginResponse) -> bool:
        ...

    @abstractmethod
    def _create_login_request(self, username: str, password: str) -> LoginRequest:
        ...

    async def login(
        self, username: str = DEFAULT_USERNAME, password: str = DEFAULT_PASSWORD
    ) -> bool:
        """attempt to log into device"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_login_request(username, password)
            ):
                if isinstance(response, LoginResponse):
                    return await self._process_login(response)

                if isinstance(response, CommandErrorResponse):
                    response.throw("Login request failed")

        raise ReolinkResponseError("Login request failed")

    @abstractmethod
    def _create_logout_request(self) -> LogoutRequest:
        ...

    @abstractmethod
    def _clear_login(self) -> None:
        ...

    async def logout(self) -> None:
        """Clear authentication information"""

        if not self.is_authenticated:
            return

        try:
            if isinstance(self, connection.Connection):
                async for response in self._execute(self._create_logout_request()):
                    if isinstance(response, CommandErrorResponse):
                        response.throw("Logout request failed")

                    if isinstance(response, ResponseCode):
                        return

            raise ReolinkResponseError("Logout request failed")
        finally:
            try:
                for callback in self._logout_callbacks:
                    if inspect.iscoroutinefunction(callback):
                        await callback()
                    else:
                        callback()
            finally:
                # whether clean or not logout always succeeds
                self._clear_login()

    @abstractmethod
    def _create_get_user_request(self) -> GetUserRequest:
        ...

    async def get_users(self):
        """Get Device Users"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(self._create_get_user_request()):
                if isinstance(response, GetUserResponse):
                    return response.users

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get PTZ Zoom Focus failed")

        raise ReolinkResponseError("Get PTZ Zoom Focus failed")
