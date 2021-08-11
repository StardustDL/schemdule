
from types import MethodType

from schemdule.prompters.builders import PrompterBuilder

from . import MessageBoxPrompter, __version__


def useMessageBox(self, auto_close: bool = False, final: bool = False) -> PrompterBuilder:
    return self.use(MessageBoxPrompter(auto_close, final))


PrompterBuilder.useMessageBox = useMessageBox
