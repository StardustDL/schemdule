import functools
import json
import logging
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from time import sleep
from typing import Any, Iterable, List, Optional, Union

import click

import enlighten

from ..prompters import (CyclePayload, Payload, PayloadCollection, Prompter,
                         SchedulePayload, UserPayload)
from ..schemas.timetable import TimeTable, TimeTableItem
from ..timeutils import subtract_time, time_to_today


@dataclass(frozen=True)
class ScheduledTimeTableItem:
    raw: TimeTableItem
    index: int
    startTime: datetime
    endTime: datetime

    def buildPayloads(self) -> PayloadCollection:
        payloads = PayloadCollection().withPayload(
            SchedulePayload(self.index, self.raw.message, self.startTime, self.endTime))

        if self.raw.cycleIndex is not None:
            payloads.withPayload(CyclePayload(
                self.raw.cycleWork, self.raw.cycleIndex))

        if isinstance(self.raw.payload, PayloadCollection):
            for payload in self.raw.payload:
                if payload is not None:
                    payloads.withPayload(payload)
        elif isinstance(self.raw.payload, Payload):
            payloads.withPayload(self.raw.payload)
        elif self.raw.payload is not None:
            payloads.withPayload(UserPayload(self.raw.payload))

        return payloads


class Scheduler:
    _logger = logging.getLogger("Scheduler")

    def __init__(self, enableIcon: bool = True) -> None:
        self._STR_PENDING = "⏳" if enableIcon else "Pending:"
        self._STR_ATTENTION = "📣" if enableIcon else "Attention:"
        self._STR_OUTDATED = "📌" if enableIcon else "Outdated:"

    def scheduledTimeTable(self, timetable: TimeTable) -> Iterable[ScheduledTimeTableItem]:
        items: List[TimeTableItem] = list(sorted(timetable.items))
        totalLen = len(items)
        for index, item in enumerate(items):
            nextItem = None if index + \
                1 >= totalLen else items[index + 1]
            yield ScheduledTimeTableItem(item, index, time_to_today(
                item.time), time_to_today(nextItem.time if nextItem else item.time))

    def schedule(self, timetable: TimeTable, prompter: Optional[Prompter] = None) -> None:
        from ..helpers import buildMessage

        def outdating(item: ScheduledTimeTableItem) -> bool:
            now = datetime.now().time()

            raw = item.raw

            if raw.time < now:
                self._logger.info(f"Outdated: {item}.")
                click.echo(f"{self._STR_OUTDATED} {buildMessage(item)}")
                return True

            return False

        def pending(item: ScheduledTimeTableItem, status: enlighten.StatusBar, manager: enlighten.Manager) -> bool:
            now = datetime.now().time()

            raw = item.raw

            if raw.time <= now:
                return False

            self._logger.info(f"Pending: {raw}.")

            message = buildMessage(item)

            status.update(f"{self._STR_PENDING} {message}")
            deltaNow = subtract_time(raw.time, now)
            pendingTotal = int(round(deltaNow.total_seconds()))

            with manager.counter(
                    total=pendingTotal, desc="", unit='ticks', leave=False) as pbar:

                while True:
                    now = datetime.now().time()
                    if raw.time <= now:
                        self._logger.info(f"Occurring: {raw}.")
                        click.echo(f"{self._STR_ATTENTION} {message}")

                        result = prompter.prompt(item.buildPayloads())
                        self._logger.info(f"Prompting result: {result}.")
                        return True
                    else:
                        delta = subtract_time(raw.time, now)
                        count = int(round(delta.total_seconds()))
                        pbar.update((pbar.total - count) - pbar.count)
                    sleep(1)

            return False

        self._logger.info(f"Start scheduling.")
        click.echo(f"Started Time: {datetime.now().time()}")

        prompter = timetable.prompter if prompter is None else prompter

        if prompter is None:
            from ..schemas import default_prompter_builder
            prompter = default_prompter_builder().build()

        self._logger.info(f"Used prompter: {prompter}.")

        with enlighten.get_manager() as manager:
            with manager.status_bar('Status',
                                    color='white_on_cyan',
                                    justify=enlighten.Justify.CENTER, leave=False) as status:

                for scheduled in self.scheduledTimeTable(timetable):
                    while True:
                        if outdating(scheduled):
                            break
                        elif pending(scheduled, status, manager):
                            break
