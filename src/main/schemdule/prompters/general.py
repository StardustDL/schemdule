from enum import auto
from typing import Any
import click

from . import Prompter, PromptResult
import PySimpleGUI as sg


class TkinterMessageBoxPrompter(Prompter):
    def prompt(self, message: str, payload: Any) -> Any:
        import tkinter
        import tkinter.messagebox

        top = tkinter.Tk()
        top.withdraw()
        tkinter.messagebox.showinfo(f"Attention {message}", payload)
        top.destroy()

        return PromptResult.Resolved


class MessageBoxPrompter(Prompter):
    def __init__(self, auto_close=False) -> None:
        super().__init__()
        self.auto_close = auto_close

    def prompt(self, message: str, payload: Any) -> Any:
        sg.popup_scrolled(str(payload), title=f"Attention {message}", auto_close=self.auto_close,
                          keep_on_top=True, background_color='white', text_color='black')

        return PromptResult.Resolved


class ConsolePrompter(Prompter):
    def prompt(self, message: str, payload: Any) -> Any:
        click.echo(f"Attention {message}: {payload}")

        return PromptResult.Resolved
