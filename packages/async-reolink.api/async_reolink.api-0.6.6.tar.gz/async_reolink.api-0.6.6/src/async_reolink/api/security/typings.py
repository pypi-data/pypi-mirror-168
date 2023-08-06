"""Security Typings"""

from asyncio import Protocol
from enum import Enum, auto


class LevelTypes(Enum):
    """User Level Types"""

    GUEST = auto()
    USER = auto()
    ADMIN = auto()


class UserInfo(Protocol):
    """User Record"""

    user_name: str
    level: LevelTypes
