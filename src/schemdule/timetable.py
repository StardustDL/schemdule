from datetime import date, time, datetime, timedelta
from typing import Optional

import functools
from queue import deque
import enlighten
import click
import json
import logging

from time import sleep

from .prompters import Prompter
from .timeutils import to_timedelta, subtract_time


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
        _start = datetime(2000, 1, 1) + to_timedelta(start)
        _end = datetime(2000, 1, 1) + to_timedelta(end)
        _work_duration = to_timedelta(work_duration)
        _rest_duration = to_timedelta(rest_duration)

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
        click.echo(f"Started Time: {datetime.now().time()}")

        if prompter is None:
            from .prompters.general import TkinterPrompter
            prompter = TkinterPrompter()

        items = deque(sorted(self.items))

        with enlighten.get_manager() as manager:

            pbar: Optional[enlighten.Counter] = None
            lastItem: Optional[TimeTableItem] = None

            status = manager.status_bar('Static Message',
                                        color='white_on_cyan',
                                        justify=enlighten.Justify.CENTER, leave=False)

            def outdating():
                nonlocal lastItem

                now = datetime.now().time()

                while len(items) > 0:
                    item = items[0]
                    if item.time < now:
                        click.echo(f"Outdated: {item.message} @ {item.time}")
                        lastItem = item
                        items.popleft()
                    else:
                        break

            def pending():
                nonlocal pbar
                if len(items) > 0:
                    item: TimeTableItem = items[0]
                    status.update(f"Pending: {item.message} @ {item.time}")
                    now = datetime.now()
                    deltaNow = subtract_time(item.time, now.time())
                    pendingTotal = int(round(deltaNow.total_seconds()))
                    if pendingTotal > 0:
                        pbar = manager.counter(
                            total=pendingTotal, desc="", unit='ticks', leave=False)

            def clear():
                nonlocal pbar

                if pbar is not None:
                    pbar.close()
                    pbar = None

            outdating()
            pending()

            while len(items) > 0:
                now = datetime.now().time()
                item: TimeTableItem = items[0]
                if item.time <= now:
                    clear()

                    click.echo(f"Attention: {item.message} @ {item.time}")
                    prompter.prompt(item.message)
                    items.popleft()
                    outdating()
                    pending()
                else:
                    if pbar is not None:
                        delta = subtract_time(item.time, now)
                        count = int(round(delta.total_seconds()))
                        pbar.update((pbar.total - count) - pbar.count)

                sleep(1)

            clear()
            status.close()
