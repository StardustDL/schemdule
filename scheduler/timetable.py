from datetime import date, time, datetime, timedelta
from typing import Optional

from .prompters import Prompter
import functools
from queue import deque

from time import sleep

import json

import logging


@functools.total_ordering
class TimeTableItem:
    def __init__(self, time: time, message: str = "") -> None:
        self.time = time
        self.message = message

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

    def at(self, time: time, message: str = "") -> None:
        self.items.append(TimeTableItem(time, message))

    def cycle(self, start: time, end: time, work_duration: time, rest_duration: time, message: str = "") -> None:
        _start = datetime(2000, 1, 1) + timedelta(hours=start.hour, minutes=start.minute,
                                               seconds=start.second, microseconds=start.microsecond)
        _end = datetime(2000, 1, 1) + timedelta(hours=end.hour, minutes=end.minute,
                                             seconds=end.second, microseconds=end.microsecond)
        _work_duration = timedelta(hours=work_duration.hour, minutes=work_duration.minute,
                                   seconds=work_duration.second, microseconds=work_duration.microsecond)
        _rest_duration = timedelta(hours=rest_duration.hour, minutes=rest_duration.minute,
                                   seconds=rest_duration.second, microseconds=rest_duration.microsecond)

        index = 0

        current = _start

        while current < _end:
            index += 1
            self.at(min(current, _end).time(),
                    f"{message} (cycle {index} starting)")
            current += _work_duration
            self.at(min(current, _end).time(),
                    f"{message} (cycle {index} resting starting)")
            current += _rest_duration
            self.at(min(current, _end).time(),
                    f"{message} (cycle {index} ending)")

    def load(self, src: str) -> None:
        def at(time_str: str, message: str):
            self.at(time(*list(map(int, time_str.split(':')))), message)

        def cycle(start_str: str, end_str: str, work_duration_str: str, rest_duration_str: str, message: str):
            self.cycle(
                time(*list(map(int, start_str.split(':')))),
                time(*list(map(int, end_str.split(':')))),
                time(*list(map(int, work_duration_str.split(':')))),
                time(*list(map(int, rest_duration_str.split(':')))),
                message)

        exec(src, {"at": at, "cycle": cycle})

    def schedule(self, prompter: Optional[Prompter] = None) -> None:
        now = datetime.now().time()

        print(f"Started Time: {now}")

        items = deque()

        for item in sorted(self.items):
            if item.time < now:
                print(f"Outdated: {item.message} @ {item.time}")
            else:
                items.append(item)

        if prompter is None:
            from .prompters.general import TkinterPrompter
            prompter = TkinterPrompter()

        if len(items) > 0:
            print(f"Pending: {items[0].message} @ {items[0].time}")

        while len(items) > 0:
            now = datetime.now().time()
            item: TimeTableItem = items[0]
            if item.time <= now:
                print(f"Attention: {item.message} @ {item.time}")
                prompter.prompt(item.message)
                items.popleft()
                if len(items) > 0:
                    print(f"Pending: {items[0].message} @ {items[0].time}")
            sleep(1)
