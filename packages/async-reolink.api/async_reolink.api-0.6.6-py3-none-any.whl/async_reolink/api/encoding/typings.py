"""Encoding typings"""

from typing import Mapping, Protocol

from async_reolink.api.typings import StreamTypes


class StreamEncodingInfo(Protocol):
    """Stream Encoding"""

    bit_rate: int
    frame_rate: int
    gop: int
    height: int
    width: int
    profile: str
    size: str
    video_type: str


class EncodingInfo(Protocol):
    """Encoding Info"""

    audio: bool
    stream: Mapping[StreamTypes, StreamEncodingInfo]
