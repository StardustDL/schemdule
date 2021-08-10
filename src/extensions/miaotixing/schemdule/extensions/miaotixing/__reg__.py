
from schemdule.prompters.builder import PrompterBuilder
from . import MiaotixingPrompter
from types import MethodType
from . import __version__


def useMiaotixing(self, code: str, final: bool = False) -> PrompterBuilder:
    return self.use(MiaotixingPrompter(code, final))


PrompterBuilder.useMiaotixing = useMiaotixing
