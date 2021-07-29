from abc import ABC, abstractmethod
from typing import Any, Iterable, Optional
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


class PrompterPayload(ABC):
    pass


class PrompterPayloadCollection(PrompterPayload):
    def __init__(self, payloads: Optional[list[Any]]) -> None:
        self.payloads = payloads if payloads is not None else []

    def try_get(self, type: type) -> Iterable[Any]:
        for item in self.payloads:
            if isinstance(item, type):
                yield item
