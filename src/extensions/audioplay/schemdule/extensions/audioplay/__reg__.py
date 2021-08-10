
from typing import Any, Callable, Iterator
from schemdule.prompters.configer import PrompterConfiger
from . import AudioPlayerPrompter
from types import MethodType
from . import __version__


def useAudioPlayer(self, files: Callable[[Any], Iterator[str]], final: bool = False) -> PrompterConfiger:
    return self.use(AudioPlayerPrompter(files, final))


PrompterConfiger.useAudioPlayer = useAudioPlayer
