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
from schemdule.prompters import (Prompter, PrompterPayload,
                                 PrompterPayloadCollection, PromptResult)

__version__ = "0.0.8"


@dataclass
class AudioPayload(PrompterPayload):
    files: List[str] = field(default_factory=list)


class AudioPlayerPrompter(Prompter):
    _logger = logging.getLogger("AudioPlayerPrompter")

    def __init__(self, final: bool = False) -> None:
        super().__init__(final)

    def prompt(self, payloads: PrompterPayloadCollection) -> PromptResult:
        schedule = payloads.getSchedule()

        audios: List[AudioPayload] = list(payloads.tryGet(AudioPayload))

        if len(audios) == 0:
            return PromptResult.Unsupported

        for audio in audios:
            if datetime.now() >= schedule.endTime:
                break

            for file in audio.files:
                if datetime.now() >= schedule.endTime:
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
                    sleep(1)
                    if datetime.now() >= schedule.endTime:
                        play_obj.stop()

        return self.success()
