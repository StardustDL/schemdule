
from schemdule.prompters.configer import PrompterConfiger
from . import MessageBoxPrompter
from types import MethodType
from . import __version__


def useMessageBox(self, auto_close: bool = False, final: bool = False) -> PrompterConfiger:
    return self.use(MessageBoxPrompter(auto_close, final))


PrompterConfiger.useMessageBox = useMessageBox
