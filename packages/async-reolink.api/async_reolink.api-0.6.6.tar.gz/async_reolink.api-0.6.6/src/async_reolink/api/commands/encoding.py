"""Encoding Commands"""

from abc import ABC

from ..encoding.typings import EncodingInfo
from . import CommandRequest, CommandResponse, ChannelValue


class GetEncodingRequest(CommandRequest, ChannelValue, ABC):
    """Get Encoding"""


class GetEncodingResponse(CommandResponse, ChannelValue, ABC):
    """Get Encoding Response"""

    info: EncodingInfo
