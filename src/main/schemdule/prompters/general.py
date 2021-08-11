from enum import auto
from typing import Any

import click

from . import Prompter, PrompterPayloadCollection, PromptResult, getMessage


class TkinterMessageBoxPrompter(Prompter):
    def __init__(self, final: bool = False) -> None:
        super().__init__(final)

    def prompt(self, payloads: PrompterPayloadCollection) -> PromptResult:
        import tkinter
        import tkinter.messagebox

        top = tkinter.Tk()
        top.withdraw()

        tkinter.messagebox.showinfo(
            f"Attention {getMessage(payloads)}", payloads)
        top.destroy()

        return self.success()


class ConsolePrompter(Prompter):
    def __init__(self, final: bool = False) -> None:
        super().__init__(final)

    def prompt(self, payloads: PrompterPayloadCollection) -> PromptResult:
        click.echo(f"Attention {getMessage(payloads)}: {payloads}")

        return self.success()


class CallablePrompter(Prompter):
    def __init__(self, final: bool = False) -> None:
        super().__init__(final)

    def prompt(self, payloads: PrompterPayloadCollection) -> PromptResult:
        hasCallable = False
        for payload in payloads.getUsers():
            if callable(payload):
                payload()
                hasCallable = True
        return self.success() if hasCallable else PromptResult.Unsupported
