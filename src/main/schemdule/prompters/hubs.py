from typing import Any
from . import Prompter, PromptResult, PrompterHub


class PrompterSwitcher(PrompterHub):
    def __init__(self, final: bool = False) -> None:
        super().__init__(final)
        self.prompters: list[Prompter] = []

    def register(self, prompter: Prompter) -> None:
        self.prompters.append(prompter)

    def prompt(self, message: str, payload: Any) -> Any:
        results = []

        for prompter in self.prompters:
            result = prompter.prompt(message, payload)

            if not isinstance(result, PromptResult):
                result = PromptResult.Empty

            results.append(result)

            if result is PromptResult.Finished:
                break
            elif result is PromptResult.Failed:
                return PromptResult.Failed

        lr = len(results)

        if lr == 0:
            return PromptResult.Empty
        elif len([x for x in results if x is PromptResult.Unsupported]) == lr:
            return PromptResult.Unsupported
        elif len([x for x in results if x is PromptResult.Empty]) == lr:
            return PromptResult.Empty
        else:
            return self.success()


class PrompterBroadcaster(PrompterHub):
    def __init__(self, final: bool = False) -> None:
        super().__init__(final)
        self.prompters: list[Prompter] = []

    def register(self, prompter: Prompter) -> None:
        self.prompters.append(prompter)

    def prompt(self, message: str, payload: Any) -> Any:
        for prompter in self.prompters:
            result = prompter.prompt(message, payload)

            if result is PromptResult.Failed:
                return PromptResult.Failed

        return self.success()
