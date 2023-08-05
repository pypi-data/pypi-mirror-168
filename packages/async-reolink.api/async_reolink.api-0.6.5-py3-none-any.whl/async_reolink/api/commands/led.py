"""LED Commands"""

from abc import ABC

from ..led.typings import LightStates, WhiteLedInfo
from . import ChannelValue, CommandRequest, CommandResponse


class GetIrLightsRequest(CommandRequest, ChannelValue, ABC):
    """Get IR Lights"""


class GetIrLightsResponse(CommandResponse, ChannelValue, ABC):
    """Get IR Lights Response"""

    state: LightStates


class SetIrLightsRequest(CommandRequest, ChannelValue, ABC):
    """Set Ir Lights"""

    state: LightStates


class GetPowerLedRequest(CommandRequest, ChannelValue, ABC):
    """Get Power Led"""


class GetPowerLedResponse(CommandResponse, ChannelValue, ABC):
    """Get Power Led Response"""

    state: LightStates


class SetPowerLedRequest(CommandRequest, ChannelValue, ABC):
    """Set Power Led"""

    state: LightStates


class GetWhiteLedRequest(CommandRequest, ChannelValue, ABC):
    """Get White Led"""


class GetWhiteLedResponse(CommandResponse, ChannelValue, ABC):
    """Get White Led Response"""

    info: WhiteLedInfo


class SetWhiteLedRequest(CommandRequest, ChannelValue, ABC):
    """Set White Led"""

    info: WhiteLedInfo
