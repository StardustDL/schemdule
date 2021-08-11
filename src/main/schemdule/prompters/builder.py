from typing import Optional

from . import Prompter, PrompterHub
from .general import (CallablePrompter, ConsolePrompter,
                      TkinterMessageBoxPrompter)
from .hubs import PrompterBroadcaster, PrompterSwitcher


class PrompterBuilder:
    """Builder for prompter."""

    def __init__(self) -> None:
        self._result: Optional[Prompter] = None

    def use(self, prompter: Prompter) -> "PrompterBuilder":
        """Use a prompter."""
        if self._result is None:
            self._result = prompter
        elif isinstance(self._result, PrompterHub):
            self._result.register(prompter)
        else:
            raise Exception(
                f"The prompter is set to a no-hub prompter {type(self._result)}.")
        return self

    def useBroadcaster(self, final: bool = False) -> "PrompterBuilder":
        """Use broadcaster as hub."""
        return self.use(PrompterBroadcaster(final))

    def useSwitcher(self, final: bool = False) -> "PrompterBuilder":
        """Use switcher as hub."""
        return self.use(PrompterSwitcher(final))

    def useConsole(self, final: bool = False) -> "PrompterBuilder":
        """Use console prompter."""
        return self.use(ConsolePrompter(final))

    def useCallable(self, final: bool = False) -> "PrompterBuilder":
        """Use callable prompter."""
        return self.use(CallablePrompter(final))

    def useTkinterMessageBox(self, final: bool = False) -> "PrompterBuilder":
        """Use Tkinter message box prompter."""
        return self.use(TkinterMessageBoxPrompter(final))

    def clear(self) -> "PrompterBuilder":
        """Clear all prompters."""
        self._result = None
        return self

    def build(self) -> Optional[Prompter]:
        """Build the final prompter."""
        return self._result
