from enum import auto
from typing import Any

import click

from . import Prompter, PrompterPayloadCollection, PromptResult


class TkinterMessageBoxPrompter(Prompter):
    def __init__(self, final: bool = False) -> None:
        super().__init__(final)

    def prompt(self, payloads: PrompterPayloadCollection) -> PromptResult:
        import tkinter
        import tkinter.messagebox
        from ..helpers import buildMessage

        top = tkinter.Tk()
        top.withdraw()

        tkinter.messagebox.showinfo(
            f"Attention {buildMessage(payloads)}", str(payloads))
        top.destroy()

        return self.success()


class ConsolePrompter(Prompter):
    def __init__(self, final: bool = False) -> None:
        super().__init__(final)

    def prompt(self, payloads: PrompterPayloadCollection) -> PromptResult:
        from ..helpers import buildMessage

        click.echo(f"Attention {buildMessage(payloads)}: {payloads}")

        return self.success()


class CallablePrompter(Prompter):
    def __init__(self, final: bool = False) -> None:
        super().__init__(final)

    def prompt(self, payloads: PrompterPayloadCollection) -> PromptResult:
        hasCallable = False
        for payload in payloads.getUsers():
            if callable(payload.payload):
                payload.payload()
                hasCallable = True
        return self.success() if hasCallable else PromptResult.Unsupported
