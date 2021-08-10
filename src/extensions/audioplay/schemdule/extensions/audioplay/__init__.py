from typing import Any, Callable, Iterator
import logging
from enum import Enum
from datetime import time, timedelta
import random
from pydub import AudioSegment, playback
import simpleaudio
import glob
from schemdule.prompters import Prompter, PromptResult

__version__ = "0.0.8"


class AudioPlayerPrompter(Prompter):
    _logger = logging.getLogger("AudioPlayerPrompter")

    def __init__(self, files: Callable[[Any], Iterator[str]], final: bool = False) -> None:
        super().__init__(final)
        self.files = files

    def prompt(self, message: str, payload: Any) -> Any:
        files = self.files(payload)

        for file in files:
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
            play_obj.wait_done()

        return self.success()

class AudioSelectorStrategy(Enum):
    Random = 0


class AudioSelectorBuilder:
    def __init__(self) -> None:
        self.files: list[str] = []
        self.strategy: AudioSelectorStrategy = AudioSelectorStrategy.Random
    
    def fromGlob(self, rule: str) -> "AudioSelectorBuilder":
        self.files = glob.glob(rule)
        return self
    
    def useRandom(self) -> "AudioSelectorBuilder":
        self.strategy = AudioSelectorStrategy.Random
        return self
    
    def build(self) -> Callable[[Any], Iterator[str]]:
        def randomSelector(payload: Any) -> Iterator[str]:
            result = [x for x in self.files]
            random.shuffle(result)
            return result
        return randomSelector
