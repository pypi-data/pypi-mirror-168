"""Record typings"""

from datetime import date
from typing import Annotated, Iterable, Iterator, Protocol

from ..typings import StreamTypes, DateTimeValue


class Search(Protocol):
    """Recording Search"""

    status_only: bool
    stream_type: StreamTypes
    start: DateTimeValue
    end: DateTimeValue


class SearchStatus(Protocol):
    """Recording Search Status"""

    year: int
    month: Annotated[int, range(1, 12)]
    days: Iterable[Annotated[int, range(1, 31)]]

    def __iter__(self) -> Iterator[date]:
        ...


class File(Protocol):
    """Recoding File"""

    frame_rate: int
    width: int
    height: int
    name: str
    size: int
    type: str
    start: DateTimeValue
    end: DateTimeValue
