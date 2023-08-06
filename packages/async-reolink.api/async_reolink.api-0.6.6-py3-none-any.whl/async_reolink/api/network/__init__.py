"""Network 3.3"""
from __future__ import annotations
from abc import ABC, abstractmethod

from ..errors import ReolinkResponseError

from ..commands import CommandErrorResponse, CommandResponse, network

from ..typings import StreamTypes

from .. import connection, system


class Network(ABC):
    """Network commands Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__link = None
        self.__ports = None
        self.__no_get_rtsp = None

        if isinstance(self, connection.Connection):
            self._disconnect_callbacks.append(self.__clear)

    def __clear(self):
        self.__no_get_rtsp = False
        self.__link = None
        self.__ports = None

    @abstractmethod
    def _create_get_local_link_request(self) -> network.GetLocalLinkRequest:
        ...

    async def get_local_link(self):
        """Get Local Link"""

        self.__link = None
        if isinstance(self, connection.Connection):
            async for response in self._execute(self._create_get_local_link_request()):
                if isinstance(response, network.GetLocalLinkResponse):
                    link = response.local_link
                    self.__link = link
                    return link

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get local link failed")

        raise ReolinkResponseError("Get local link failed")

    @abstractmethod
    def _create_get_channel_status_request(self) -> network.GetChannelStatusRequest:
        ...

    async def get_channel_status(self):
        """Get Channel Statuses"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_get_channel_status_request()
            ):
                if isinstance(response, network.GetChannelStatusResponse):
                    return response.channels

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get channel status failed")

        raise ReolinkResponseError("Get channel status failed")

    @abstractmethod
    def _create_get_ports_request(self) -> network.GetNetworkPortsRequest:
        ...

    async def get_ports(self):
        """Get Network Ports"""

        self.__ports = None
        if isinstance(self, connection.Connection):
            async for response in self._execute(self._create_get_ports_request()):
                if isinstance(response, network.GetNetworkPortsResponse):
                    ports = response.ports
                    self.__ports = ports
                    return ports

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get network ports failed")

        raise ReolinkResponseError("Get network ports failed")

    async def _ensure_ports_and_link(self):

        commands = []
        if self.__link is None:
            if isinstance(self, system.System):
                abilities = await self._ensure_abilities()
                if abilities.local_link:
                    commands.append(self._create_get_local_link_request())
            else:
                commands.append(self._create_get_local_link_request())
        if self.__ports is None:
            commands.append(self._create_get_ports_request())

        if not commands:
            return
        if isinstance(self, connection.Connection):
            responses = self.batch(commands)
        else:
            return

        async for response in responses:
            if isinstance(response, network.GetLocalLinkResponse):
                self.__link = response.local_link
            elif isinstance(response, network.GetNetworkPortsResponse):
                self.__ports = response.ports

    @abstractmethod
    def _create_get_rtsp_urls_request(
        self, channel_id: int = 0
    ) -> network.GetRTSPUrlsRequest:
        ...

    async def get_rtsp_url(
        self, channel: int = 0, stream: StreamTypes = StreamTypes.MAIN
    ):
        """Get RTSP Url"""

        if self.__no_get_rtsp is None:
            self.__no_get_rtsp = True
            if isinstance(self, system.System):
                abilities = await self._ensure_abilities()
                self.__no_get_rtsp = (
                    abilities.schedule_version.value
                    == system.capabilities.ScheduleVersion.BASIC
                )

        if not self.__no_get_rtsp:
            if isinstance(self, connection.Connection):
                async for response in self._execute(
                    self._create_get_rtsp_urls_request(0)
                ):
                    if isinstance(response, network.GetRTSPUrlsResponse):
                        return response.urls[stream]

            self.__no_get_rtsp = True

        await self._ensure_ports_and_link()

        port = (
            f":{self.__ports.rtsp.value}"
            if self.__ports.rtsp.value not in (0, 554)
            else ""
        )

        url = f"rtsp://{self.__link.ip.address}{port}/h264Preview_{(channel+1):02}_{stream.name.lower()}"
        return url

    async def get_rtmp_url(
        self, channel: int = 0, stream: StreamTypes = StreamTypes.MAIN
    ):
        """Get RTMP Url"""

        await self._ensure_ports_and_link()

        port = (
            f":{self.__ports.rtmp.value}"
            if self.__ports.rtmp.value not in (0, 1935)
            else ""
        )

        url = f"rtmp://{self.__link.ip.address}{port}/bcs/channel{channel}_{stream.name.lower()}.bcs?channel={channel}&stream={stream.name.lower()}"
        return url

    @abstractmethod
    def _create_get_p2p_request(self) -> network.GetP2PRequest:
        ...

    async def get_p2p(self):
        """Get P2P"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(self._create_get_p2p_request()):
                if isinstance(response, network.GetP2PResponse):
                    return response.info

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get p2p info failed")

        raise ReolinkResponseError("Get p2p info failed")

    def _create_get_wifi_info_request(self) -> network.GetWifiInfoRequest:
        ...

    async def get_wifi(self):
        """Get Wifi Info"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(self._create_get_wifi_info_request()):
                if isinstance(response, network.GetWifiInfoResponse):
                    return response.info

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get wifi info failed")

        raise ReolinkResponseError("Get wifi info failed")

    def _create_get_wifi_signal_request(self) -> network.GetWifiSignalRequest:
        ...

    async def get_wifi_signal(self):
        """Get Wifi Signal Strength"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(self._create_get_wifi_signal_request()):
                if isinstance(response, network.GetWifiSignalResponse):
                    return response.signal

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get wifi signal failed")

        raise ReolinkResponseError("Get wifi signal failed")
