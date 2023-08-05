"""Commands"""

from typing import Any, Protocol, runtime_checkable

from ..errors import ReolinkResponseError

# pylint: disable=too-few-public-methods


class CommandResponse(Protocol):
    """Command Response"""


@runtime_checkable
class ResponseCode(Protocol):
    """Command Response Code"""

    response_code: int


class ChannelValue(Protocol):
    """Channel Value"""

    channel_id: int


class ErrorResponseValue(Protocol):
    """Error Response Value"""

    error_code: int
    details: str | None


@runtime_checkable
class CommandErrorResponse(CommandResponse, ErrorResponseValue, Protocol):
    """Command Error Response"""

    def throw(self, *args):
        """throw as error"""
        raise ReolinkResponseError(*args, code = self.error_code, details= self.details)


class CommandRequest(Protocol):
    """Command Request"""
