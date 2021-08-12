
from datetime import timedelta
from types import MethodType
from typing import Optional

from schemdule.prompters.builders import PrompterBuilder

from . import MessageBoxPrompter, __version__


def useMessageBox(self, autoClose: bool = False, maxKeep: Optional[timedelta] = None, final: bool = False) -> PrompterBuilder:
    if maxKeep is None:
        maxKeep = timedelta(minutes=1)
    return self.use(MessageBoxPrompter(autoClose, maxKeep, final))


PrompterBuilder.useMessageBox = useMessageBox
