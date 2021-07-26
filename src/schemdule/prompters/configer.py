from typing import Optional


from . import Prompter, PrompterHub
from .hubs import PrompterBroadcaster, PrompterSwitcher
from .general import ConsolePrompter, TkinterMessageBoxPrompter, MessageBoxPrompter


class PrompterConfiger:
    def __init__(self) -> None:
        self._result: Optional[Prompter] = None

    def use(self, prompter: Prompter) -> "PrompterConfiger":
        if self._result is None:
            self._result = prompter
        elif isinstance(self._result, PrompterHub):
            self._result.register(prompter)
        else:
            raise Exception(
                f"The prompter is set to a no-hub prompter {type(self._result)}.")
        return self

    def useBroadcaster(self) -> "PrompterConfiger": return self.use(PrompterBroadcaster())

    def useSwitcher(self) -> "PrompterConfiger": return self.use(PrompterSwitcher())

    def useConsole(self) -> "PrompterConfiger": return self.use(ConsolePrompter())

    def useTkinterMessageBox(self) -> "PrompterConfiger": return self.use(TkinterMessageBoxPrompter())

    def useMessageBox(self, auto_close=False) -> "PrompterConfiger": return self.use(MessageBoxPrompter(auto_close))

    def build(self) -> Prompter:
        return self._result

