
from typing import Any, Callable, Iterator
from schemdule.prompters.builder import PrompterBuilder
from . import AudioPlayerPrompter
from types import MethodType
from . import __version__


def useAudioPlayer(self, files: Callable[[Any], Iterator[str]], final: bool = False) -> PrompterBuilder:
    return self.use(AudioPlayerPrompter(files, final))


PrompterBuilder.useAudioPlayer = useAudioPlayer
