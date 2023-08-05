"""AI Commands"""

from abc import ABC
from typing import Mapping, MutableMapping

from ..ai.typings import AlarmState, AITypes, Config

from . import CommandRequest, CommandResponse, ChannelValue


class GetAiStateRequest(CommandRequest, ChannelValue, ABC):
    """Get AI State"""


class GetAiStateResponse(CommandResponse, ChannelValue, ABC):
    """Get AI State Response"""

    state: Mapping[AITypes, AlarmState]


class GetAiConfigRequest(CommandRequest, ChannelValue, ABC):
    """Get AI Configuration"""


class GetAiConfigResponse(CommandResponse, ChannelValue, ABC):
    """Get AI Configuration Response"""

    config: Config


class SetAiConfigRequest(CommandRequest, ChannelValue, ABC):
    """Set AI Configuration"""

    detect_type: MutableMapping[AITypes, bool]
    ai_track: bool
    track_type: MutableMapping[AITypes, bool]
