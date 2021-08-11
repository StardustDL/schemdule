
from types import MethodType
from typing import Any, Callable, Iterable, Iterator, List, Optional

from schemdule.prompters.builders import PayloadBuilder, PrompterBuilder

from . import AudioPayload, AudioPlayerPrompter, __version__


def useAudioPlayer(self: PrompterBuilder, final: bool = False) -> PrompterBuilder:
    return self.use(AudioPlayerPrompter(final))


def useAudio(self: PayloadBuilder, files: Iterable[str]) -> PayloadBuilder:
    return self.use(AudioPayload(list(files)))


PrompterBuilder.useAudioPlayer = useAudioPlayer
PayloadBuilder.useAudio = useAudio
