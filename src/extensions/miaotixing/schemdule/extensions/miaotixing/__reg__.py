
from schemdule.prompters.configer import PrompterConfiger
from . import MiaotixingPrompter
from types import MethodType
from . import __version__


def useMiaotixing(self, code: str, final: bool = False) -> PrompterConfiger:
    return self.use(MiaotixingPrompter(code, final))


PrompterConfiger.useMiaotixing = useMiaotixing
