
from schemdule.prompters.configer import PrompterConfiger
from . import MessageBoxPrompter
from types import MethodType

def useMessageBox(self, auto_close=False) -> PrompterConfiger: return self.use(MessageBoxPrompter(auto_close))

def schemaPrompter(prompter: PrompterConfiger) -> None:
    prompter.useMessageBox = MethodType(useMessageBox, prompter)