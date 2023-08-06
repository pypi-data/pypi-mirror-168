"""Network Commands"""

from abc import ABC
from typing import Mapping
from . import ChannelValue, CommandRequest, CommandResponse

from ..network.typings import ChannelStatus, LinkInfo, NetworkPorts, P2PInfo, WifiInfo

from ..typings import StreamTypes


class GetLocalLinkRequest(CommandRequest, ABC):
    """Get Local Link Request"""


class GetLocalLinkResponse(CommandResponse, ABC):
    """Get Local Link Response"""

    local_link: LinkInfo


class GetChannelStatusRequest(CommandRequest, ABC):
    """Get Channel Status Request"""


class GetChannelStatusResponse(CommandResponse, ABC):
    """Get Channel Status Response"""

    channels: Mapping[int, ChannelStatus]


class GetNetworkPortsRequest(CommandRequest, ABC):
    """Get Network Ports Request"""


class GetNetworkPortsResponse(CommandResponse, ABC):
    """Get Network Ports Response"""

    ports: NetworkPorts


class GetRTSPUrlsRequest(CommandRequest, ChannelValue, ABC):
    """Get RTSP URls Request"""


class GetRTSPUrlsResponse(CommandResponse, ChannelValue, ABC):
    """Get RTSP Urls Repsonse"""

    urls: Mapping[StreamTypes, str]


class GetP2PRequest(CommandRequest, ABC):
    """Get P2P Info Request"""


class GetP2PResponse(CommandResponse, ABC):
    """Get P2P Info Response"""

    info: P2PInfo


class GetWifiInfoRequest(CommandRequest, ABC):
    """Get Wifi Info Request"""


class GetWifiInfoResponse(CommandResponse, ABC):
    """Get Wifi Info Response"""

    info: WifiInfo


class GetWifiSignalRequest(CommandRequest, ABC):
    """Get Wifi Signal Strength Request"""


class GetWifiSignalResponse(CommandRequest, ABC):
    """Get Wifi Signal Stength Response"""

    signal: int
