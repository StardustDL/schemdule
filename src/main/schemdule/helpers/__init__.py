
import functools
import json
import logging
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from time import sleep
from typing import Any, Iterable, List, Optional, Union

import click

import enlighten

from ..prompters import PrompterPayloadCollection
from ..schedulers import ScheduledTimeTableItem

EMOJI_TIME = ["🕛🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚", "🕧🕜🕝🕞🕟🕠🕡🕢🕣🕤🕥🕦"]
EMOJI_BELL = "🔔"
EMOJI_WORK = "💼"
EMOJI_REST = "☕"


def buildMessage(payloads: Union[PrompterPayloadCollection, ScheduledTimeTableItem], cycle: bool = True, icon: bool = True) -> str:
    if isinstance(payloads, ScheduledTimeTableItem):
        return buildMessage(payloads.buildPayloads(), cycle=cycle, icon=icon)

    schedule = payloads.getSchedule()

    iconStartTime = EMOJI_TIME[0 if schedule.startTime.minute <
                               30 else 1][schedule.startTime.hour % 12]
    iconEndTime = EMOJI_TIME[0 if schedule.endTime.minute <
                             30 else 1][schedule.endTime.hour % 12]
    iconHead = EMOJI_BELL

    schedule = payloads.getSchedule()
    message = schedule.message

    if cycle:
        cycleP = payloads.getCycle()
        if cycleP:
            iconHead = EMOJI_WORK if cycleP.work else EMOJI_REST
            message += f" (cycle {cycleP.index} {'' if cycleP.work else 'resting '}starting)"

    if icon:
        return f"{iconHead} {message} {iconStartTime} {schedule.startTime.time()} - {iconEndTime} {schedule.endTime.time()}"
    else:
        return f"{message} {schedule.startTime.time()} - {schedule.endTime.time()}"
