import logging
from typing import Any

from . import PayloadCollection, Prompter, PrompterHub, PromptResult


class PrompterSwitcher(PrompterHub):
    _logger = logging.getLogger("PrompterSwitcher")

    def __init__(self, final: bool = False) -> None:
        super().__init__(final)
        self.prompters: list[Prompter] = []

    def register(self, prompter: Prompter) -> None:
        self._logger.debug(f"Register: {prompter}.")
        self.prompters.append(prompter)

    def prompt(self, payloads: PayloadCollection) -> PromptResult:
        results = []
        schedule = payloads.getSchedule()
        for prompter in self.prompters:
            self._logger.info(
                f"Send '{schedule.message}' to prompter: {prompter}.")

            result = prompter.prompt(payloads)

            self._logger.info(f"Recieved {result} from prompter {prompter}.")

            results.append(result)

            if result is PromptResult.Finished:
                self._logger.info(
                    f"Finish prompting for '{schedule.message}'.")
                break
            elif result is PromptResult.Failed:
                self._logger.error(
                    f"Failed prompting for '{schedule.message}' at prompter {prompter}.")
                return PromptResult.Failed

        lr = len(results)

        if lr == 0 or len([x for x in results if x is PromptResult.Empty]) == lr:
            self._logger.info(f"Empty prompting for '{schedule.message}'.")
            return PromptResult.Empty
        elif len([x for x in results if x is PromptResult.Unsupported]) == lr:
            self._logger.info(
                f"Unsupported prompting for '{schedule.message}'.")
            return PromptResult.Unsupported
        else:
            self._logger.info(f"Success prompting for '{schedule.message}'.")
            return self.success()


class PrompterBroadcaster(PrompterHub):
    _logger = logging.getLogger("PrompterBroadcaster")

    def __init__(self, final: bool = False) -> None:
        super().__init__(final)
        self.prompters: list[Prompter] = []

    def register(self, prompter: Prompter) -> None:
        self._logger.debug(f"Register: {prompter}.")
        self.prompters.append(prompter)

    def prompt(self, payloads: PayloadCollection) -> PromptResult:
        schedule = payloads.getSchedule()
        for prompter in self.prompters:
            self._logger.info(
                f"Send '{schedule.message}' to prompter: {prompter}.")

            result = prompter.prompt(payloads)

            self._logger.info(f"Recieved {result} from prompter {prompter}.")

            if result is PromptResult.Failed:
                self._logger.error(
                    f"Failed prompting for '{schedule.message}' at prompter {prompter}.")
                return PromptResult.Failed

        self._logger.info(f"Success prompting for '{schedule.message}'.")
        return self.success()
