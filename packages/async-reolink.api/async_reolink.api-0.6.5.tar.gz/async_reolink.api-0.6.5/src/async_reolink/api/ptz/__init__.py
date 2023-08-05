"""PTZ 3.7"""

from abc import ABC, abstractmethod

from .. import connection
from ..commands import CommandErrorResponse, ResponseCode, ptz

from ..errors import ReolinkResponseError

from ..ptz.typings import Operation, Preset, Patrol, Track, ZoomOperation


class PTZ(ABC):
    """PTZ commands Mixin"""

    @abstractmethod
    def _create_get_ptz_presets_request(self, channel: int) -> ptz.GetPresetRequest:
        ...

    async def get_ptz_presets(self, channel: int = 0):
        """Get PTZ Presets"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_get_ptz_presets_request(channel)
            ):
                if isinstance(response, ptz.GetPresetResponse):
                    return response.presets

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get PTZ Presets failed")

        raise ReolinkResponseError("Get PTZ Presets failed")

    @abstractmethod
    def _create_set_ptz_preset_request(self, preset: Preset) -> ptz.SetPresetRequest:
        ...

    async def set_ptz_preset(self, preset: Preset):
        """Set PTZ Preset"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_set_ptz_preset_request(preset)
            ):
                if isinstance(response, CommandErrorResponse):
                    response.throw("Set PTZ Preset failed")

                if isinstance(response, ResponseCode):
                    return True

        raise ReolinkResponseError("Set PTZ Preset failed")

    @abstractmethod
    def _create_get_ptz_patrols_request(self, channel: int) -> ptz.GetPatrolRequest:
        ...

    async def get_ptz_patrols(self, channel: int = 0):
        """Get PTZ Patrols"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_get_ptz_patrols_request(channel)
            ):
                if isinstance(response, ptz.GetPatrolResponse):
                    return response.patrols

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get PTZ Patrols failed")

        raise ReolinkResponseError("Get PTZ Patrols failed")

    @abstractmethod
    def _create_set_ptz_patrol_request(self, patrol: Patrol) -> ptz.SetPatrolRequest:
        ...

    async def set_ptz_patrol(self, patrol: Patrol):
        """Set PTZ Patrol"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_set_ptz_patrol_request(patrol)
            ):
                if isinstance(response, CommandErrorResponse):
                    response.throw("Set PTZ Preset failed")

                if isinstance(response, ResponseCode):
                    return True

        raise ReolinkResponseError("Set PTZ Preset failed")

    @abstractmethod
    def _create_get_ptz_tatterns_request(self, channel: int) -> ptz.GetTatternRequest:
        ...

    async def get_ptz_tatterns(self, channel: int = 0):
        """Get PTZ Tatterns"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_get_ptz_tatterns_request(channel)
            ):
                if isinstance(response, ptz.GetTatternResponse):
                    return response.tracks

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get PTZ Tatterns failed")

        raise ReolinkResponseError("Get PTZ Tatterns failed")

    @abstractmethod
    def _create_set_ptz_tatterns_request(
        self, channel: int, *track: Track
    ) -> ptz.SetTatternRequest:
        ...

    async def set_ptz_tattern(self, *tracks: Track, channel: int = 0):
        """Set PTZ Tattern"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_set_ptz_tatterns_request(channel, *tracks)
            ):
                if isinstance(response, CommandErrorResponse):
                    response.throw("Set PTZ Tattern failed")

                if isinstance(response, ResponseCode):
                    return True

        raise ReolinkResponseError("Set PTZ Tattern failed")

    @abstractmethod
    def _create_set_ptz_control_request(
        self,
        channel: int,
        operation: Operation,
        speed: int | None,
        preset_id: int | None,
    ) -> ptz.SetControlRequest:
        ...

    async def ptz_control(
        self,
        operation: Operation,
        speed: int | None = None,
        preset_id: int | None = None,
        channel: int = 0,
    ):
        """PTZ Control"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_set_ptz_control_request(
                    channel, operation, speed, preset_id
                )
            ):
                if isinstance(response, CommandErrorResponse):
                    response.throw("Set PTZ Control failed")

                if isinstance(response, ResponseCode):
                    return True

        raise ReolinkResponseError("Set PTZ Control failed")

    @abstractmethod
    def _create_get_ptz_autofocus_request(
        self, channel: int
    ) -> ptz.GetAutoFocusRequest:
        ...

    async def get_ptz_autofocus(self, channel: int = 0):
        """Get PTZ AutoFocus"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_get_ptz_autofocus_request(channel)
            ):
                if isinstance(response, ptz.GetAutoFocusResponse):
                    return not response.disabled

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get PTZ AutoFocus failed")

        raise ReolinkResponseError("Get PTZ AutoFocus failed")

    @abstractmethod
    def _create_set_ptz_autofocus_request(
        self, channel: int, disabled: bool
    ) -> ptz.SetAutoFocusRequest:
        ...

    async def set_ptz_autofocus(self, disabled: bool, channel: int = 0):
        """Set PTZ AutoFocus"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_set_ptz_autofocus_request(channel, disabled)
            ):
                if isinstance(response, CommandErrorResponse):
                    response.throw("Set PTZ AutoFocus failed")

                if isinstance(response, ResponseCode):
                    return True

        raise ReolinkResponseError("Set PTZ AutoFocus failed")

    @abstractmethod
    def _create_get_ptz_zoom_focus_request(
        self, channel: int
    ) -> ptz.GetZoomFocusRequest:
        ...

    async def get_ptz_zoom_focus(self, channel: int = 0):
        """Get PTZ Zoom and Focus"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_get_ptz_zoom_focus_request(channel)
            ):
                if isinstance(response, ptz.GetZoomFocusResponse):
                    return response.state

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get PTZ Zoom Focus failed")

        raise ReolinkResponseError("Get PTZ Zoom Focus failed")

    @abstractmethod
    def _create_set_ptz_zoomfocus_request(
        self, channel: int, operation: ZoomOperation, position: int
    ) -> ptz.SetZoomFocusRequest:
        ...

    async def set_ptz_zoomfocus(
        self,
        position: int,
        operation: ZoomOperation = ZoomOperation.ZOOM,
        channel: int = 0,
    ):
        """Set PTZ Zoom"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_set_ptz_zoomfocus_request(channel, operation, position)
            ):
                if isinstance(response, CommandErrorResponse):
                    response.throw("Set PTZ Zoom/Focus failed")

                if isinstance(response, ResponseCode):
                    return True

        raise ReolinkResponseError("Set PTZ Zoom/Focus failed")
