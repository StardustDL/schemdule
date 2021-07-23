import tkinter
import tkinter.messagebox
import click

from . import Prompter


class TkinterPrompter(Prompter):
    def prompt(self, message: str) -> None:
        top = tkinter.Tk()
        top.withdraw()
        tkinter.messagebox.showinfo("Attention", message)
        top.destroy()

class ConsolePrompter(Prompter):
    def prompt(self, message: str) -> None:
        click.echo(f"Attention: {message}")
