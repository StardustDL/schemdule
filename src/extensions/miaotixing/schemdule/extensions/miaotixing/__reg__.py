
from types import MethodType

from schemdule.prompters.builders import PrompterBuilder

from . import MiaotixingPrompter, __version__


def useMiaotixing(self, code: str, final: bool = False) -> PrompterBuilder:
    return self.use(MiaotixingPrompter(code, final))


PrompterBuilder.useMiaotixing = useMiaotixing
