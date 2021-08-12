import functools
import logging
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from re import L
from typing import Any, Callable, Optional, Union

from schemdule.prompters.builders import PayloadBuilder

from ..prompters import Prompter
from ..timeutils import parse_time, subtract_time, to_timedelta


@dataclass(order=True, frozen=True)
class TimeTableItem:
    time: time
    message: str = ""
    payload: Any = None
    cycleIndex: Optional[int] = None
    cycleWork: bool = False


class TimeTable:
    _logger = logging.getLogger("TimeTable")

    def __init__(self) -> None:
        self.items: list[TimeTableItem] = []
        self.prompter: Optional[Prompter] = None

    def use(self, prompter: Optional[Prompter]) -> None:
        self._logger.debug(f"Use prompter {prompter}.")
        self.prompter = prompter

    def at(self, time: time, message: str = "", payload: Any = None, cycleIndex: Optional[int] = None, cycleWork: bool = False) -> None:
        """
        Register an event at time with message.

        If payload is a PayloadBuilder, Schemdule will build the final payload automaticly.
        """
        self._logger.debug(f"{message} ({payload}) at {time}.")

        if isinstance(payload, PayloadBuilder):
            payload = payload.build()

        self.items.append(TimeTableItem(
            time, message, payload, cycleIndex, cycleWork))

    def cycle(self, start: time, end: time, workDuration: timedelta, restDuration: timedelta, message: str = "", workPayload: Optional[Callable[[int], Any]] = None, restPayload: Optional[Callable[[int], Any]] = None) -> None:
        self._logger.debug(
            f"{message} ({workPayload}, {restPayload}) cycle from {start} to {end} (work {workDuration}, rest {restDuration}).")

        if workPayload is None:
            def workPayload(_): return None
        if restPayload is None:
            def restPayload(_): return None

        _start = datetime(2000, 1, 1) + to_timedelta(start)
        _end = datetime(2000, 1, 1) + to_timedelta(end)

        index = 0

        current = _start

        while current < _end:
            index += 1
            self.at(min(current, _end).time(),
                    message, workPayload(index), index, True)
            current += workDuration
            self.at(min(current, _end).time(),
                    message, restPayload(index), index, False)
            current += restDuration

    def clear(self) -> None:
        self.items.clear()
