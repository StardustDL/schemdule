from abc import ABC, abstractmethod


class Prompter(ABC):
    @abstractmethod
    def prompt(self, message: str) -> None:
        pass
