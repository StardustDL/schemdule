from enum import auto
from typing import Any
import click

from . import Prompter, PromptResult


class TkinterMessageBoxPrompter(Prompter):
    def __init__(self, final: bool = False) -> None:
        super().__init__(final)

    def prompt(self, message: str, payload: Any) -> Any:
        import tkinter
        import tkinter.messagebox

        top = tkinter.Tk()
        top.withdraw()
        tkinter.messagebox.showinfo(f"Attention {message}", payload)
        top.destroy()

        return self.success()


class ConsolePrompter(Prompter):
    def __init__(self, final: bool = False) -> None:
        super().__init__(final)

    def prompt(self, message: str, payload: Any) -> Any:
        click.echo(f"Attention {message}: {payload}")

        return self.success()


class CallablePrompter(Prompter):
    def __init__(self, final: bool = False) -> None:
        super().__init__(final)

    def prompt(self, message: str, payload: Any) -> Any:
        if callable(payload):
            result = payload()
            if isinstance(result, PromptResult):
                return result
            return self.success()
        return PromptResult.Unsupported
