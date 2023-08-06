"""System"""
from __future__ import annotations
from abc import ABC, abstractmethod
from ctypes import cast
from datetime import datetime
from typing import TYPE_CHECKING

from .typings import DeviceInfo

from .capabilities import Capabilities

from ..errors import ReolinkResponseError


from ..commands import CommandErrorResponse, ResponseCode
from ..commands.system import (
    GetAbilitiesRequest,
    GetAbilitiesResponse,
    GetDeviceInfoRequest,
    GetDeviceInfoResponse,
    GetTimeRequest,
    GetTimeResponse,
    RebootRequest,
    GetHddInfoRequest,
    GetHddInfoResponse,
)

from .. import connection


class System(ABC):
    """System Commands Mixin"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__abilities = None
        self.__time = None
        self.__timezone = None

        if isinstance(self, connection.Connection):
            self._disconnect_callbacks.append(self.__clear)

    def __clear(self):
        self.__abilities = None
        self.__timezone = None
        self.__time = None

    @abstractmethod
    def _create_get_capabilities_request(
        self, username: str | None
    ) -> GetAbilitiesRequest:
        ...

    @abstractmethod
    def _create_empty_capabilities(self) -> Capabilities:
        ...

    async def get_ability(self, username: str | None = None):
        """Get User Permisions"""

        if username is None:
            self.__abilities = None

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_get_capabilities_request(username)
            ):
                if isinstance(response, GetAbilitiesResponse):
                    return response.capabilities

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get capabilities failed")

        return self._create_empty_capabilities()

    async def _ensure_abilities(self):
        if self.__abilities:
            return self.__abilities
        return await self.get_ability()

    @abstractmethod
    def _create_get_device_info_request(self) -> GetDeviceInfoRequest:
        ...

    @abstractmethod
    def _create_empty_device_info(self) -> DeviceInfo:
        ...

    async def get_device_info(self):
        """Get Device Information"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(self._create_get_device_info_request()):
                if isinstance(response, GetDeviceInfoResponse):
                    return response.info

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get device info failed")

        return self._create_empty_device_info()

    @abstractmethod
    def _create_get_time_request(self) -> GetTimeRequest:
        ...

    async def get_time(self):
        """Get Device Time Information"""

        self.__timezone = None
        self.__time = None

        if isinstance(self, connection.Connection):
            async for response in self._execute(self._create_get_time_request()):
                if isinstance(response, GetTimeResponse):
                    self.__time = response.to_datetime()
                    self.__timezone = response.to_timezone()

                    return self.__time

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get time failed")

        if TYPE_CHECKING:
            _time = datetime.now()
            self.__time = _time
        return self.__time

    async def _ensure_time(self):
        if self.__time:
            return self.__time
        return await self.get_time()

    async def get_time_info(self):
        """Get DST Info"""
        await self._ensure_time()
        if TYPE_CHECKING:
            _tz = datetime.now().tzinfo
            if _tz is None:
                raise TypeError()
            self.__timezone = _tz
        return self.__timezone

    @abstractmethod
    def _create_reboot_request(self) -> RebootRequest:
        ...

    async def reboot(self):
        """Reboot device"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(self._create_reboot_request()):
                if isinstance(response, ResponseCode):
                    return True

                if isinstance(response, CommandErrorResponse):
                    response.throw("Reboot failed")

        raise ReolinkResponseError("Reboot failed")

    @abstractmethod
    def _create_get_hdd_info_request(self) -> GetHddInfoRequest:
        ...

    async def get_storage_info(self):
        """Get Device Recording Capabilities"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(self._create_get_hdd_info_request()):
                if isinstance(response, GetHddInfoResponse):
                    return response.info

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get storage Info failed")

        raise ReolinkResponseError("Get storage Info failed")
