"""Security Commands"""

from abc import ABC
from . import CommandRequest, CommandResponse


class LoginRequest(CommandRequest, ABC):
    """Login Request"""

    user_name: str
    password: str


class LoginResponse(CommandResponse, ABC):
    """Login Response"""


class LogoutRequest(CommandRequest, ABC):
    """Logout Request"""
