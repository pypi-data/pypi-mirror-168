"""LED 3.10"""

from abc import ABC, abstractmethod
from typing import Mapping, Sequence

from ..ai.typings import AITypes

from ..led.typings import LightStates, LightingSchedule, WhiteLedInfo

from ..typings import PercentValue

from .. import connection, ai
from ..commands import CommandErrorResponse, ResponseCode, led

from ..errors import ReolinkResponseError


class LED(ABC):
    """LED Mixin"""

    @abstractmethod
    def _create_get_ir_lights_request(self, channel: int) -> led.GetIrLightsRequest:
        ...

    async def get_ir_lights(self, channel: int = 0):
        """Get IR Light State Info"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_get_ir_lights_request(channel)
            ):
                if (
                    isinstance(response, led.GetIrLightsResponse)
                    and response.channel_id == channel
                ):
                    return response.state

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get IR Lights failed")

        raise ReolinkResponseError("Get IR Lights failed")

    @abstractmethod
    def _create_set_ir_lights_request(
        self, state: LightStates, channel: int
    ) -> led.SetIrLightsRequest:
        ...

    async def set_ir_lights(self, state: LightStates, channel: int = 0):
        """Set IR Light State"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_set_ir_lights_request(state, channel)
            ):
                if isinstance(response, CommandErrorResponse):
                    response.throw("Set IR Lights failed")

                if isinstance(response, ResponseCode):
                    return True

        raise ReolinkResponseError("Set IR Lights failed")

    @abstractmethod
    def _create_get_power_led_request(self, channel: int) -> led.GetPowerLedRequest:
        ...

    async def get_power_led(self, channel: int = 0):
        """Get Power Led State Info"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_get_power_led_request(channel)
            ):
                if (
                    isinstance(response, led.GetPowerLedResponse)
                    and response.channel_id == channel
                ):
                    return response.state

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get Power Led failed")

        raise ReolinkResponseError("Get Power Led failed")

    @abstractmethod
    def _create_set_power_led_request(
        self, state: LightStates, channel: int
    ) -> led.SetPowerLedRequest:
        ...

    async def set_power_led(self, state: LightStates, channel: int):
        """Set Power Led State"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_set_power_led_request(state, channel)
            ):
                if isinstance(response, CommandErrorResponse):
                    response.throw("Set Power Led failed")

                if isinstance(response, ResponseCode):
                    return True

        raise ReolinkResponseError("Set Power Led failed")

    @abstractmethod
    def _create_get_white_led_request(self, channel: int) -> led.GetWhiteLedRequest:
        ...

    async def get_white_led(self, channel: int = 0):
        """Get White Led State Info"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_get_power_led_request(channel)
            ):
                if (
                    isinstance(response, led.GetWhiteLedResponse)
                    and response.channel_id == channel
                ):
                    return response.info

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get White Led failed")

        raise ReolinkResponseError("Get White Led failed")

    @abstractmethod
    def _create_set_white_led_request(
        self,
        info: WhiteLedInfo,
        channel: int,
    ) -> led.SetWhiteLedRequest:
        ...

    async def set_white_led(
        self,
        value: WhiteLedInfo,
        channel: int = 0,
    ):
        """Set White Led State"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_set_white_led_request(value, channel)
            ):
                if isinstance(response, CommandErrorResponse):
                    response.throw("Set White Led failed")

                if isinstance(response, ResponseCode):
                    return True

        raise ReolinkResponseError("Set White Led failed")
