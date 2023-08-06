"""Record Commands"""

from abc import ABC
from typing import Sequence

from ..record.typings import Search, SearchStatus, File

from . import CommandRequest, ChannelValue, CommandResponse


class GetSnapshotRequest(CommandRequest, ChannelValue, ABC):
    """Get Snapshot Request"""


class SearchRecordingsRequest(CommandRequest, ChannelValue, ABC):
    """Search Recordings Request"""

    search: Search


class SearchRecordingsResponse(CommandResponse, ChannelValue, ABC):
    """Search Recordings Response"""

    status: Sequence[SearchStatus] | None
    files: Sequence[File] | None
