
from types import MethodType
from typing import Any, Callable, Iterator

from schemdule.prompters.builder import PrompterBuilder

from . import AudioPlayerPrompter, __version__


def useAudioPlayer(self, final: bool = False) -> PrompterBuilder:
    return self.use(AudioPlayerPrompter(final))


PrompterBuilder.useAudioPlayer = useAudioPlayer
