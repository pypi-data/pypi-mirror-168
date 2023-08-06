"""PTZ Typings"""
from enum import Enum, auto
from typing import Annotated, Protocol, Sequence

from ..typings import size


class ZoomFocus(Protocol):
    """PTZ Zoom/Focus"""

    zoom: Annotated[int, range(1, 64)]
    focus: Annotated[int, range(1, 64)]


class Preset(Protocol):
    """PTZ Preset"""

    id: Annotated[int, range(1, 64)]  # pylint: disable=invalid-name
    """Integer within 1 and 64"""
    name: Annotated[str, size(31)]
    """String max length of 31"""
    enabled: bool | None = None


class PatrolPreset(Protocol):
    """PTZ Patrol Preset"""

    dwell_time: Annotated[int, range(1, 30)]  # pylint: disable=invalid-name
    """Dwell Time for preset of 1 to 30 seconds"""
    preset_id: int
    speed: Annotated[int, range(1, 64)]
    """Patrol speed for preset within 1 to 64"""


class Patrol(Protocol):
    """PTZ Patrol"""

    enabled: bool
    id: Annotated[int, range(1, 64)]  # pylint: disable=invalid-name
    """Integer within 1 and 64"""
    name: Annotated[str, size(31)]
    """String max length of 31"""
    presets: Sequence[PatrolPreset]
    running: bool | None


class Operation(Enum):
    """PTZ Operations"""

    STOP = auto()
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    LEFT_UP = auto()
    LEFT_DOWN = auto()
    RIGHT_UP = auto()
    RIGHT_DOWN = auto()
    IRIS_SHRINK = auto()
    IRIS_ENLARGE = auto()
    ZOOM_OUT = auto()
    ZOOM_IN = auto()
    FOCUS_BACK = auto()
    FOCUS_FORWARD = auto()
    AUTO = auto()
    PATROL_START = auto()
    PATROL_STOP = auto()
    TO_PRESET = auto()


class Track(Protocol):
    """PTZ Track"""

    id: Annotated[int, range(1, 6)]  # pylint: disable=invalid-name
    """Integer within 1 and 6"""
    name: Annotated[str, size(191)] | None
    """String max length of 191"""
    enabled: bool | None
    running: bool | None


class ZoomOperation(Enum):
    """Zoom Operation"""

    ZOOM = auto()
    FOCUS = auto()
