"""AI Typings"""

from enum import Enum, auto
from typing import Mapping, Protocol


class AITypes(Enum):
    """AI Types"""

    ANIMAL = auto()
    PET = auto()
    FACE = auto()
    PEOPLE = auto()
    VEHICLE = auto()


class AlarmState(Protocol):
    """Alarm State"""

    state: bool
    supported: bool


class Config(Protocol):
    """Configuration"""

    detect_type: Mapping[AITypes, bool]
    ai_track: bool
    track_type: Mapping[AITypes, bool]
