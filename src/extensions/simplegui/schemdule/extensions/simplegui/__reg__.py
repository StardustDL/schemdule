
from schemdule.prompters.configer import PrompterConfiger
from . import MessageBoxPrompter
from types import MethodType


def useMessageBox(self, final: bool = False, auto_close: bool = False) -> PrompterConfiger:
    return self.use(MessageBoxPrompter(final, auto_close))


PrompterConfiger.useMessageBox = useMessageBox
