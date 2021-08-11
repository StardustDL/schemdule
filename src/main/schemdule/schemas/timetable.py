from datetime import date, time, datetime, timedelta
from typing import Optional, Union, Any

import functools
import logging

from ..prompters import Prompter
from ..timeutils import to_timedelta, subtract_time, parse_time


@functools.total_ordering
class TimeTableItem:
    def __init__(self, time: time, message: str = "", payload: Any = None, cycleIndex: Optional[int] = None, cycleWork: bool = False) -> None:
        self.time = time
        self.message = message
        self.payload = payload
        self.cycleIndex = cycleIndex
        self.cycleWork = cycleWork

    def __eq__(self, other: object) -> bool:
        if isinstance(other, TimeTableItem):
            return (self.time, self.message) == (other.time, other.message)
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, TimeTableItem):
            return self.time < other.time
        return NotImplemented

    def __repr__(self) -> str:
        return f"TimeTableItem({self.time}, {self.message})"


class TimeTable:
    _logger = logging.getLogger("TimeTable")

    def __init__(self) -> None:
        self.items: list[TimeTableItem] = []
        self.prompter: Optional[Prompter] = None

    def use(self, prompter: Optional[Prompter]) -> None:
        self._logger.debug(f"Use prompter {prompter}.")
        self.prompter = prompter

    def at(self, time: time, message: str = "", payload: Any = None, cycleIndex: Optional[int] = None, cycleWork: bool = False) -> None:
        self._logger.debug(f"{message} ({payload}) at {time}.")
        self.items.append(TimeTableItem(time, message, payload, cycleIndex, cycleWork))

    def cycle(self, start: time, end: time, work_duration: timedelta, rest_duration: timedelta, message: str = "", work_payload: Any = None, rest_payload: Any = None) -> None:
        self._logger.debug(
            f"{message} ({work_payload}, {rest_payload}) cycle from {start} to {end} (work {work_duration}, rest {rest_duration}).")
        _start = datetime(2000, 1, 1) + to_timedelta(start)
        _end = datetime(2000, 1, 1) + to_timedelta(end)

        index = 0

        current = _start

        while current < _end:
            index += 1
            self.at(min(current, _end).time(),
                    message, work_payload, index, True)
            current += work_duration
            self.at(min(current, _end).time(),
                    message, rest_payload, index, False)
            current += rest_duration

    def clear(self) -> None:
        self.items.clear()
