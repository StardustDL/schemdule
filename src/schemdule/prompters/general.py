import tkinter
import tkinter.messagebox
from typing import Any
import click

from . import Prompter, PromptResult


class TkinterPrompter(Prompter):
    def prompt(self, message: str, payload: Any) -> Any:
        top = tkinter.Tk()
        top.withdraw()
        tkinter.messagebox.showinfo(f"Attention {message}", payload)
        top.destroy()

        return PromptResult.Resolved


class ConsolePrompter(Prompter):
    def prompt(self, message: str, payload: Any) -> Any:
        click.echo(f"Attention {message}: {payload}")

        return PromptResult.Resolved
