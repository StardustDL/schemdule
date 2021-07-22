from datetime import date, time, datetime, timedelta
from typing import Optional

from click.core import Option

from .prompters import Prompter
import functools
from queue import deque
import enlighten
import click

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

        click.echo(f"Started Time: {now}")

        items = deque()

        pbar: Optional[enlighten.Counter] = None
        lastItem: Optional[TimeTableItem] = None

        for item in sorted(self.items):
            if item.time < now:
                click.echo(f"Outdated: {item.message} @ {item.time}")
                lastItem = item
            else:
                items.append(item)

        if prompter is None:
            from .prompters.general import TkinterPrompter
            prompter = TkinterPrompter()

        def pending():
            nonlocal pbar
            if len(items) > 0:
                item: TimeTableItem = items[0]
                click.echo(f"Pending: {item.message} @ {item.time}")
                last = datetime.now()
                if lastItem is not None:
                    last = datetime(year=last.year, month=last.month, day=last.day,
                                   hour=lastItem.time.hour, minute=lastItem.time.minute, second=lastItem.time.second, microsecond=lastItem.time.microsecond)
                delta = datetime(year=last.year, month=last.month, day=last.day,
                                 hour=item.time.hour, minute=item.time.minute, second=item.time.second, microsecond=item.time.microsecond) - last
                pendingTotal = int(round(delta.total_seconds()))
                if pbar is None and pendingTotal > 0:
                    pbar = enlighten.Counter(
                        total=pendingTotal, desc=item.message, unit='ticks')

        pending()

        while len(items) > 0:
            now = datetime.now()
            item: TimeTableItem = items[0]
            if item.time <= now.time():
                if pbar is not None:
                    pbar.close(clear=True)
                    pbar = None
                click.echo(f"Attention: {item.message} @ {item.time}")
                prompter.prompt(item.message)
                items.popleft()
                pending()
            else:
                if pbar is not None:
                    pending: TimeTableItem = items[0]
                    delta = datetime(year=now.year, month=now.month, day=now.day,
                                     hour=item.time.hour, minute=item.time.minute, second=item.time.second, microsecond=item.time.microsecond) - now
                    count = int(round(delta.total_seconds()))
                    pbar.update((pbar.total - count) - pbar.count)

            sleep(1)

        if pbar is not None:
            pbar.close(clear=True)
            pbar = None
