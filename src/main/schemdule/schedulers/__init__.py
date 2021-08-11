from dataclasses import dataclass
from datetime import date, time, datetime, timedelta
from typing import Optional, Union, Any

import functools
from queue import deque
import enlighten
import click
import json
import logging

from time import sleep
from ..prompters import CyclePayload, Prompter, PrompterPayloadCollection, SchedulePayload, UserPayload
from ..schemas.timetable import TimeTable, TimeTableItem
from ..schemas import default_prompter_builder
from ..timeutils import subtract_time


@dataclass
class ScheduledTimeTableItem:
    raw: TimeTableItem
    index: int
    duration: timedelta


class Scheduler:
    _logger = logging.getLogger("Scheduler")

    def schedule(self, timetable: TimeTable, prompter: Optional[Prompter] = None) -> None:
        def outdating(item: ScheduledTimeTableItem) -> bool:
            now = datetime.now().time()

            if item.time < now:
                self._logger.info(f"Outdated: {item}.")
                click.echo(f"Outdated: {item.raw.message} @ {item.raw.time}")
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
                            SchedulePayload(item.index, raw.message, item.duration))
                        
                        if raw.cycleIndex is not None:
                            payloads.withPayload(CyclePayload(raw.cycleWork, raw.cycleIndex))

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

        items = deque(sorted(timetable.items))

        with enlighten.get_manager() as manager:
            with manager.status_bar('Status',
                                    color='white_on_cyan',
                                    justify=enlighten.Justify.CENTER, leave=False) as status:

                totalLen = len(items)
                for index, item in enumerate(items):
                    while True:
                        if outdating(item):
                            break
                        elif pending(item, status, manager):
                            break
