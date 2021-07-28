from abc import ABC, abstractmethod
from typing import Any
from enum import Enum


class Prompter(ABC):
    @abstractmethod
    def prompt(self, message: str, payload: Any) -> Any:
        pass

class PrompterHub(Prompter, ABC):
    @abstractmethod
    def register(self, prompter: Prompter) -> None:
        pass


class PromptResult(Enum):
    Empty = 0
    Unsupported = 1     # Unsupported, skip this and go next
    Resolved = 2        # Resolved, go next
    Finished = 3        # Resolved, stop going next
    Failed = 4          # Failed, stop going next