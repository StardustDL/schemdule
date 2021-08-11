import functools
import json
import logging
from datetime import date, datetime, time, timedelta
from typing import Any, Dict, Optional, Union, cast

import click

import enlighten

from ..extensions import (findExtensions, loadExtension, loadExtensions,
                          useExtension, useExtensions)
from ..prompters import Prompter
from ..prompters.builders import PayloadBuilder, PrompterBuilder
from ..timeutils import parse_time, subtract_time, to_timedelta
from .timetable import TimeTable, TimeTableItem


def default_prompter_builder() -> PrompterBuilder:
    prompter = PrompterBuilder()
    prompter.useSwitcher().useConsole().useCallable(True).useTkinterMessageBox()
    return prompter


class SchemaBuilder:
    _logger = logging.getLogger("SchemaBuilder")

    def __init__(self) -> None:
        self.result: TimeTable = TimeTable()

    def getEnv(self) -> Dict[str, Any]:
        prompterBuilder = default_prompter_builder()

        env = {}

        def at(raw_time: Union[str, time], message: str = "", payload: Any = None) -> None:
            ttime = parse_time(raw_time) if isinstance(
                raw_time, str) else raw_time
            if isinstance(payload, PayloadBuilder):
                payload = payload.build()
            self.result.at(ttime, message, payload)

        def cycle(raw_start: Union[str, time], raw_end: Union[str, time], raw_work_duration: Union[str, time, timedelta], raw_rest_duration: Union[str, time, timedelta], message: str = "", work_payload: Any = None, rest_payload: Any = None) -> None:
            tstart = parse_time(raw_start) if isinstance(
                raw_start, str) else raw_start
            tend = parse_time(raw_end) if isinstance(raw_end, str) else raw_end
            twork_duration = to_timedelta(parse_time(raw_work_duration)) if isinstance(
                raw_work_duration, str) else to_timedelta(raw_work_duration) if isinstance(
                raw_work_duration, time) else raw_work_duration
            trest_duration = to_timedelta(parse_time(raw_rest_duration)) if isinstance(
                raw_rest_duration, str) else to_timedelta(raw_rest_duration) if isinstance(
                raw_rest_duration, time) else raw_rest_duration

            if isinstance(work_payload, PayloadBuilder):
                work_payload = work_payload.build()
            if isinstance(rest_payload, PayloadBuilder):
                rest_payload = rest_payload.build()

            self.result.cycle(
                tstart, tend, twork_duration, trest_duration,
                message, work_payload, rest_payload)

        def payloads() -> PayloadBuilder:
            return PayloadBuilder()

        def loadRaw(source: str) -> None:
            src_preview = source[:50].replace('\n', ' ').replace('\r', ' ')
            self._logger.info(f"Load: '{src_preview}...'")
            exec(source, env)

        def load(file: str, encoding: str = "utf8") -> None:
            with open(file, encoding=encoding) as f:
                source = f.read()
            loadRaw(source)

        def ext(name: Optional[str] = None) -> None:
            if name is None:
                self._logger.info("Use all installed extensions.")
                extnames = findExtensions()
                exts = loadExtensions(extnames)
                useExtensions(exts, env)
            else:
                self._logger.info(f"Use extension {name}.")
                extension = loadExtension(name)
                useExtension(extension, env)

        env["at"] = at
        env["cycle"] = cycle
        env["load"] = load
        env["loadRaw"] = loadRaw
        env["ext"] = ext
        env["payloads"] = payloads
        env["prompter"] = prompterBuilder
        env["env"] = env

        return env

    def useEnv(self, env: Dict[str, Any]):
        prompter = env.get("prompter")
        if isinstance(prompter, PrompterBuilder):
            self.result.use(prompter.build())

    def loadWithEnv(self, src: str, env: Dict[str, Any]) -> None:
        env["loadRaw"](src)
        self.useEnv(env)

    def load(self, src) -> None:
        self.loadWithEnv(src, self.getEnv())
