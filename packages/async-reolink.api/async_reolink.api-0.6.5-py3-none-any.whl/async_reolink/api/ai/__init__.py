"""AI Mixin"""


from abc import ABC, abstractmethod
from typing import Mapping

from ..errors import ErrorCodes, ReolinkResponseError

from ..commands import CommandErrorResponse, ResponseCode
from ..commands.ai import (
    GetAiConfigRequest,
    GetAiConfigResponse,
    GetAiStateRequest,
    GetAiStateResponse,
    SetAiConfigRequest,
)

from .typings import AITypes, Config

from .. import connection


class AI(ABC):
    """AI Mixin"""

    @abstractmethod
    def _create_get_ai_state_request(self, channel: int) -> GetAiStateRequest:
        ...

    async def get_ai_state(self, channel: int = 0):
        """Get AI State Info"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_get_ai_state_request(channel)
            ):
                if (
                    isinstance(response, GetAiStateResponse)
                    and response.channel_id == channel
                ):
                    return response.state

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get AI State failed")

        raise ReolinkResponseError("Get AI State failed")

    @abstractmethod
    def _create_get_ai_config_request(self, channel: int) -> GetAiConfigRequest:
        ...

    async def get_ai_config(self, channel: int = 0):
        """Get AI Config Info"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_get_ai_config_request(channel)
            ):
                if (
                    isinstance(response, GetAiConfigResponse)
                    and response.channel_id == channel
                ):
                    return response.config

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get AI State failed")

        raise ReolinkResponseError("Get AI State failed")

    @abstractmethod
    def _create_set_ai_config(self, channel: int, config: Config) -> SetAiConfigRequest:
        ...

    async def set_ai_config(
        self,
        config: Config,
        channel: int = 0,
    ):
        """Set AI Configuration"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_set_ai_config(channel, config)
            ):
                if isinstance(response, CommandErrorResponse):
                    response.throw("Set AI State failed")

                if isinstance(response, ResponseCode):
                    return True

        raise ReolinkResponseError("Set AI State failed")
