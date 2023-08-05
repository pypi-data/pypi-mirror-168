"""Encoding"""

from abc import ABC, abstractmethod

from ..errors import ErrorCodes, ReolinkResponseError

from ..commands import CommandErrorResponse
from ..commands.encoding import GetEncodingRequest, GetEncodingResponse

from .. import connection


class Encoding(ABC):
    """Encoding Mixin"""

    @abstractmethod
    def _create_get_encoding_request(self, channel: int) -> GetEncodingRequest:
        ...

    async def get_encoding(self, channel: int = 0):
        """Get Encoding Info"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_get_encoding_request(channel)
            ):
                if (
                    isinstance(response, GetEncodingResponse)
                    and response.channel_id == channel
                ):
                    return response.info

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get AI State failed")

        raise ReolinkResponseError("Get AI State failed")
