
from schemdule.prompters.configer import PrompterConfiger
from . import MessageBoxPrompter
from types import MethodType

def useMessageBox(self, auto_close=False) -> PrompterConfiger:
    return self.use(MessageBoxPrompter(auto_close))

PrompterConfiger.useMessageBox = useMessageBox
