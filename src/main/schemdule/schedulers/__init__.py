import functools
import json
import logging
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from queue import deque
from time import sleep
from typing import Any, Optional, Union

import click

import enlighten

from ..prompters import (CyclePayload, Prompter, PrompterPayloadCollection,
                         SchedulePayload, UserPayload)
from ..schemas import default_prompter_builder
from ..schemas.timetable import TimeTable, TimeTableItem
from ..timeutils import subtract_time, time_to_today


@dataclass
class ScheduledTimeTableItem:
    raw: TimeTableItem
    index: int
    startTime: datetime
    endTime: datetime


class Scheduler:
    _logger = logging.getLogger("Scheduler")

    def schedule(self, timetable: TimeTable, prompter: Optional[Prompter] = None) -> None:
        def outdating(item: ScheduledTimeTableItem) -> bool:
            now = datetime.now().time()

            raw = item.raw

            if raw.time < now:
                self._logger.info(f"Outdated: {item}.")
                click.echo(f"Outdated: {raw.message} @ {raw.time}")
                return True

            return False

        def pending(item: ScheduledTimeTableItem, status: enlighten.StatusBar, manager: enlighten.Manager) -> bool:
            now = datetime.now().time()

            raw = item.raw

            if raw.time <= now:
                return False

            self._logger.info(f"Pending: {raw}.")
            status.update(f"Pending: {raw.message} @ {raw.time}")
            deltaNow = subtract_time(raw.time, now)
            pendingTotal = int(round(deltaNow.total_seconds()))

            with manager.counter(
                    total=pendingTotal, desc="", unit='ticks', leave=False) as pbar:

                while True:
                    now = datetime.now().time()
                    if raw.time <= now:
                        self._logger.info(f"Occurring: {raw}.")
                        click.echo(f"Attention: {raw.message} @ {raw.time}")

                        payloads = PrompterPayloadCollection().withPayload(
                            SchedulePayload(item.index, raw.message, item.startTime, item.endTime))

                        if raw.cycleIndex is not None:
                            payloads.withPayload(CyclePayload(
                                raw.cycleWork, raw.cycleIndex))

                        if isinstance(raw.payload, PrompterPayloadCollection):
                            for payload in raw.payload:
                                payloads.withPayload(UserPayload(payload))
                        else:
                            payloads.withPayload(UserPayload(raw.payload))

                        result = prompter.prompt(payloads)
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
            prompter = default_prompter_builder().build()

        self._logger.info(f"Used prompter: {prompter}.")

        items: list[TimeTableItem] = list(sorted(timetable.items))

        with enlighten.get_manager() as manager:
            with manager.status_bar('Status',
                                    color='white_on_cyan',
                                    justify=enlighten.Justify.CENTER, leave=False) as status:

                totalLen = len(items)
                for index, item in enumerate(items):
                    nextItem = None if index + \
                        1 >= totalLen else items[index + 1]
                    scheduled = ScheduledTimeTableItem(item, index, time_to_today(
                        item.time), time_to_today(nextItem.time if nextItem else item.time))
                    while True:
                        if outdating(scheduled):
                            break
                        elif pending(scheduled, status, manager):
                            break
