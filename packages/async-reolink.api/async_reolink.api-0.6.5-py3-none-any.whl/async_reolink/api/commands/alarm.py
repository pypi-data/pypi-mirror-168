"""Alarm Commands"""

from abc import ABC

from . import CommandRequest, ChannelValue, CommandResponse


class GetMotionStateRequest(CommandRequest, ChannelValue, ABC):
    """Get Motion State Request"""


class GetMostionStateResponse(CommandResponse, ABC):
    """Get Mostion State Response"""

    state: bool
