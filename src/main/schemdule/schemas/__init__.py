from datetime import date, time, datetime, timedelta
from typing import Dict, Optional, Union, Any

import functools
from queue import deque
import enlighten
import click
import json
import logging

from ..prompters import Prompter
from ..prompters.configer import PrompterConfiger
from ..extensions import load_extension, use_extension, find_extensions, load_extensions, use_extensions
from ..timeutils import to_timedelta, subtract_time, parse_time
from .timetable import TimeTable, TimeTableItem


def default_prompter_configer() -> PrompterConfiger:
    prompter = PrompterConfiger()
    prompter.useSwitcher().useConsole().useCallable(True).useTkinterMessageBox()
    return prompter


class SchemaBuilder:
    def __init__(self) -> None:
        self.result: TimeTable = TimeTable()

    def get_env(self) -> Dict[str, Any]:
        prompterConfiger = default_prompter_configer()

        env = {}

        def at(raw_time: Union[str, time], message: str = "", payload: Any = None):
            ttime = parse_time(raw_time) if isinstance(
                raw_time, str) else raw_time
            self.result.at(ttime, message, payload)

        def cycle(raw_start: Union[str, time], raw_end: Union[str, time], raw_work_duration: Union[str, time], raw_rest_duration: Union[str, time], message: str = "", payload: Any = None):
            tstart = parse_time(raw_start) if isinstance(
                raw_start, str) else raw_start
            tend = parse_time(raw_end) if isinstance(raw_end, str) else raw_end
            twork_duration = parse_time(raw_work_duration) if isinstance(
                raw_work_duration, str) else raw_work_duration
            trest_duration = parse_time(raw_rest_duration) if isinstance(
                raw_rest_duration, str) else raw_rest_duration
            self.result.cycle(
                tstart, tend, twork_duration, trest_duration,
                message, payload)

        def load(source: str):
            exec(source, env)

        def ext(name: Optional[str] = None):
            if name is None:
                extnames = find_extensions()
                exts = load_extensions(extnames)
                use_extensions(exts, env)
            else:
                extension = load_extension(name)
                use_extension(extension, env)

        env["at"] = at
        env["cycle"] = cycle
        env["load"] = load
        env["ext"] = ext
        env["prompter"] = prompterConfiger
        env["env"] = env

        return env

    def use_env(self, env: Dict[str, Any]):
        prompter = env.get("prompter")
        if isinstance(prompter, PrompterConfiger):
            self.result.use(prompter.build())

    def load_with_env(self, src: str, env: Dict[str, Any]) -> None:
        env["load"](src)
        self.use_env(env)

    def load(self, src) -> None:
        self.load_with_env(src, self.get_env())
