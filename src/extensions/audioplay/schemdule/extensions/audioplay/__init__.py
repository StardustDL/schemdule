from typing import Any, Callable, Iterator
import logging
from datetime import time, timedelta
from pydub import AudioSegment, playback
import simpleaudio
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
