"""Security Commands"""

from abc import ABC
from typing import Sequence
from . import CommandRequest, CommandResponse

from ..security import typings


class LoginRequest(CommandRequest, ABC):
    """Login Request"""

    user_name: str
    password: str


class LoginResponse(CommandResponse, ABC):
    """Login Response"""


class LogoutRequest(CommandRequest, ABC):
    """Logout Request"""


class GetUserRequest(CommandRequest, ABC):
    """Get User(s) Request"""


class GetUserResponse(CommandResponse, ABC):
    """Get User(s) Response"""

    users: Sequence[typings.UserInfo]
