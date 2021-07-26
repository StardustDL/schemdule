from typing import Optional


from . import Prompter, PrompterHub
from .hubs import PrompterBroadcaster, PrompterSwitcher
from .general import ConsolePrompter, TkinterPrompter


class PrompterConfiger:
    def __init__(self) -> None:
        self._result: Optional[Prompter] = None

    def use(self, prompter: Prompter) -> None:
        if self._result is None:
            self._result = prompter
        elif isinstance(self._result, PrompterHub):
            self._result.register(prompter)
        else:
            raise Exception(
                f"The prompter is set to a no-hub prompter {type(self._result)}.")

    def useBroadcaster(self) -> None: self.use(PrompterBroadcaster())

    def useSwitcher(self) -> None: self.use(PrompterSwitcher())

    def useConsole(self) -> None: self.use(ConsolePrompter())

    def useTkinter(self) -> None: self.use(TkinterPrompter())

    def build(self) -> Prompter:
        return self._result

