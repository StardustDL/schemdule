from enum import auto
from typing import Any
import click

from . import Prompter, PromptResult


class TkinterMessageBoxPrompter(Prompter):
    def prompt(self, message: str, payload: Any) -> Any:
        import tkinter
        import tkinter.messagebox

        top = tkinter.Tk()
        top.withdraw()
        tkinter.messagebox.showinfo(f"Attention {message}", payload)
        top.destroy()

        return PromptResult.Resolved


class ConsolePrompter(Prompter):
    def prompt(self, message: str, payload: Any) -> Any:
        click.echo(f"Attention {message}: {payload}")

        return PromptResult.Resolved
