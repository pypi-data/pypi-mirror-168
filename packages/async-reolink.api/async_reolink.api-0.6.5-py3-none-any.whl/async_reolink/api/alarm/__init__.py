"""Alarm"""

from abc import ABC, abstractmethod

from ..errors import ReolinkResponseError

from ..commands import CommandErrorResponse, alarm

from .. import connection


class Alarm(ABC):
    """Alarm Mixin"""

    @abstractmethod
    def _create_get_md_state(self, channel: int) -> alarm.GetMotionStateRequest:
        ...

    async def get_md_state(self, channel: int = 0):
        """Get Motion Detection Info"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(self._create_get_md_state(channel)):
                if isinstance(response, alarm.GetMostionStateResponse):
                    return response.state

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get Motion State failed")

        raise ReolinkResponseError("Get Motion State failed")
