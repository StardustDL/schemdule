from datetime import date, time, datetime, timedelta
from typing import Optional, Union, Any

import functools
from queue import deque
import enlighten
import click
import json
import logging

from time import sleep

from ..prompters import Prompter
from ..prompters.configer import PrompterConfiger
from ..extensions import load_extension, use_extension
from ..timeutils import to_timedelta, subtract_time, parse_time


@functools.total_ordering
class TimeTableItem:
    def __init__(self, time: time, message: str = "", payload: Any = None) -> None:
        self.time = time
        self.message = message
        self.payload = payload

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
    def __init__(self) -> None:
        self.items: list[TimeTableItem] = []
        self.prompter: Optional[Prompter] = None

    def use(self, prompter: Optional[Prompter]) -> None:
        self.prompter = prompter

    def at(self, time: time, message: str = "", payload: Any = None) -> None:
        self.items.append(TimeTableItem(time, message, payload))

    def cycle(self, start: time, end: time, work_duration: time, rest_duration: time, message: str = "", payload: Any = None) -> None:
        _start = datetime(2000, 1, 1) + to_timedelta(start)
        _end = datetime(2000, 1, 1) + to_timedelta(end)
        _work_duration = to_timedelta(work_duration)
        _rest_duration = to_timedelta(rest_duration)

        index = 0

        current = _start

        while current < _end:
            index += 1
            self.at(min(current, _end).time(),
                    f"{message} (cycle {index} starting)", payload)
            current += _work_duration
            self.at(min(current, _end).time(),
                    f"{message} (cycle {index} resting starting)", payload)
            current += _rest_duration

    def clear(self) -> None:
        self.items.clear()
