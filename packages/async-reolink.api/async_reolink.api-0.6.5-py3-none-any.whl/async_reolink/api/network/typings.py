"""Network Typings"""

from enum import Enum, auto
from typing import Protocol


class LinkTypes(Enum):
    """Link Types"""

    STATIC = auto()
    DHCP = auto()


class IPInfo(Protocol):
    """IP Info"""

    gateway: str
    address: str
    mask: str


class LinkInfo(Protocol):
    """Link Info"""

    active_link: str
    mac: str
    type: LinkTypes
    ip: IPInfo


class ChannelStatus(Protocol):
    """Channel Status"""

    channel_id: int
    name: str
    online: bool
    type: str


class P2PInfo(Protocol):
    """P2P Info"""

    enabled: bool
    uid: str


class NetworkPort(Protocol):
    """Network Port"""

    value: int
    enabled: bool


class NetworkPorts(Protocol):
    """Network Ports"""

    media: NetworkPort
    http: NetworkPort
    https: NetworkPort
    onvif: NetworkPort
    rtmp: NetworkPort
    rtsp: NetworkPort
