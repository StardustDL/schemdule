import functools
import json
import logging
from datetime import date, datetime, time, timedelta
from typing import Any, Callable, Dict, Optional, Union, cast

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

        def at(rawTime: Union[str, time], message: str = "", payload: Any = None) -> None:
            ttime = parse_time(rawTime) if isinstance(
                rawTime, str) else rawTime
            if isinstance(payload, PayloadBuilder):
                payload = payload.build()
            self.result.at(ttime, message, payload)

        def cycle(rawStart: Union[str, time], rawEnd: Union[str, time], rawWorkDuration: Union[str, time, timedelta], rawRestDuration: Union[str, time, timedelta], message: str = "", workPayload: Optional[Callable[[int], Any]] = None, restPayload: Optional[Callable[[int], Any]] = None) -> None:
            tstart = parse_time(rawStart) if isinstance(
                rawStart, str) else rawStart
            tend = parse_time(rawEnd) if isinstance(rawEnd, str) else rawEnd
            twork_duration = to_timedelta(parse_time(rawWorkDuration)) if isinstance(
                rawWorkDuration, str) else to_timedelta(rawWorkDuration) if isinstance(
                rawWorkDuration, time) else rawWorkDuration
            trest_duration = to_timedelta(parse_time(rawRestDuration)) if isinstance(
                rawRestDuration, str) else to_timedelta(rawRestDuration) if isinstance(
                rawRestDuration, time) else rawRestDuration

            self.result.cycle(
                tstart, tend, twork_duration, trest_duration,
                message, workPayload, restPayload)

        def payloads() -> PayloadBuilder:
            return PayloadBuilder()

        def prompters() -> PrompterBuilder:
            return PrompterBuilder()

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
        env["prompters"] = prompters
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
