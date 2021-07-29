from typing import Any
from . import Prompter, PromptResult, PrompterHub


class PrompterSwitcher(PrompterHub):
    def __init__(self) -> None:
        super().__init__()
        self.prompters: list[Prompter] = []

    def register(self, prompter: Prompter) -> None:
        self.prompters.append(prompter)

    def prompt(self, message: str, payload: Any) -> Any:
        results = []

        for prompter in self.prompters:
            result = prompter.prompt(message, payload)

            results.append(result)

            if result is PromptResult.Finished:
                return PromptResult.Finished
            elif result is PromptResult.Failed:
                return PromptResult.Failed

        lr = len(results)

        if lr == 0:
            return PromptResult.Empty
        elif len(filter(lambda x: x is PromptResult.Unsupported)) == lr:
            return PromptResult.Unsupported
        elif len(filter(lambda x: x is PromptResult.Empty)) == lr:
            return PromptResult.Empty
        else:
            return PromptResult.Resolved


class PrompterBroadcaster(PrompterHub):
    def __init__(self) -> None:
        super().__init__()
        self.prompters: list[Prompter] = []

    def register(self, prompter: Prompter) -> None:
        self.prompters.append(prompter)

    def prompt(self, message: str, payload: Any) -> Any:
        results = []

        for prompter in self.prompters:
            results.append(prompter.prompt(message, payload))

        return results
