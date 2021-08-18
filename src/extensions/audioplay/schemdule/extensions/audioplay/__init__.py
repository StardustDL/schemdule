import glob
import logging
import random
from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from enum import Enum
from time import sleep
from typing import Any, Callable, Iterable, Iterator, List

import simpleaudio
from pydub import AudioSegment, playback
from schemdule.configurations.globals import globalConfiguration
from schemdule.prompters import (Payload, PayloadCollection, Prompter,
                                 PromptResult, SchedulePayload)

__version__ = "0.0.11"


@dataclass
class AudioPayload(Payload):
    files: List[str] = field(default_factory=list)


class AudioPlayerPrompter(Prompter):
    _logger = logging.getLogger("AudioPlayerPrompter")

    def __init__(self, endSpace: timedelta, final: bool = False) -> None:
        super().__init__(final)
        self.endSpace = endSpace

    def _needStop(self, schedule: SchedulePayload) -> bool:
        return datetime.now() + self.endSpace + globalConfiguration.timeslice >= schedule.endTime

    def prompt(self, payloads: PayloadCollection) -> PromptResult:
        schedule = payloads.getSchedule()

        audios: List[AudioPayload] = list(payloads.tryGet(AudioPayload))

        if len(audios) == 0:
            return PromptResult.Unsupported

        for audio in audios:
            if self._needStop(schedule):
                break

            for file in audio.files:
                if self._needStop(schedule):
                    break

                self._logger.debug(f"Load file {file}...")
                sound = AudioSegment.from_file(file)
                self._logger.info(
                    f"Play audio {file} ({timedelta(seconds=sound.duration_seconds)})...")
                play_obj = simpleaudio.play_buffer(
                    sound.raw_data,
                    num_channels=sound.channels,
                    bytes_per_sample=sound.sample_width,
                    sample_rate=sound.frame_rate
                )
                while play_obj.is_playing():
                    sleep(globalConfiguration.timeslice.total_seconds())
                    if self._needStop(schedule):
                        self._logger.info(f"Stop audio {file}.")
                        play_obj.stop()

        return self.success()
