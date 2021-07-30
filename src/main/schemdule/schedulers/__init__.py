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
from ..schemas.timetable import TimeTable, TimeTableItem
from ..schemas import default_prompter_configer
from ..timeutils import subtract_time


class Scheduler:
    _logger = logging.getLogger("Scheduler")

    def schedule(self, timetable: TimeTable, prompter: Optional[Prompter] = None) -> None:
        def outdating(item: TimeTableItem) -> bool:
            now = datetime.now().time()

            if item.time < now:
                self._logger.info(f"Outdated: {item}.")
                click.echo(f"Outdated: {item.message} @ {item.time}")
                return True

            return False

        def pending(item: TimeTableItem, status: enlighten.StatusBar, manager: enlighten.Manager) -> bool:
            now = datetime.now().time()

            if item.time <= now:
                return False

            self._logger.info(f"Pending: {item}.")
            status.update(f"Pending: {item.message} @ {item.time}")
            deltaNow = subtract_time(item.time, now)
            pendingTotal = int(round(deltaNow.total_seconds()))

            with manager.counter(
                    total=pendingTotal, desc="", unit='ticks', leave=False) as pbar:

                while True:
                    now = datetime.now().time()
                    if item.time <= now:
                        self._logger.info(f"Occurring: {item}.")
                        click.echo(f"Attention: {item.message} @ {item.time}")
                        result = prompter.prompt(item.message, item.payload)
                        self._logger.info(f"Prompting result: {result}.")
                        return True
                    else:
                        delta = subtract_time(item.time, now)
                        count = int(round(delta.total_seconds()))
                        pbar.update((pbar.total - count) - pbar.count)
                    sleep(1)

            return False

        self._logger.info(f"Start scheduling.")
        click.echo(f"Started Time: {datetime.now().time()}")

        prompter = timetable.prompter if prompter is None else prompter

        if prompter is None:
            prompter = default_prompter_configer().build()

        self._logger.info(f"Used prompter: {prompter}.")

        items = deque(sorted(timetable.items))

        with enlighten.get_manager() as manager:
            with manager.status_bar('Status',
                                    color='white_on_cyan',
                                    justify=enlighten.Justify.CENTER, leave=False) as status:

                while len(items) > 0:
                    item: TimeTableItem = items[0]

                    if outdating(item):
                        items.popleft()
                    elif pending(item, status, manager):
                        items.popleft()
