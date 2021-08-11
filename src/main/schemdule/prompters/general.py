from enum import auto
from typing import Any
import click

from . import Prompter, PromptResult, PrompterPayloadCollection


class TkinterMessageBoxPrompter(Prompter):
    def __init__(self, final: bool = False) -> None:
        super().__init__(final)

    def prompt(self, payloads: PrompterPayloadCollection) -> PromptResult:
        import tkinter
        import tkinter.messagebox

        top = tkinter.Tk()
        top.withdraw()

        schedule = payloads.getSchedule()

        tkinter.messagebox.showinfo(f"Attention {schedule.message}", payloads)
        top.destroy()

        return self.success()


class ConsolePrompter(Prompter):
    def __init__(self, final: bool = False) -> None:
        super().__init__(final)

    def prompt(self, payloads: PrompterPayloadCollection) -> PromptResult:
        schedule = payloads.getSchedule()

        click.echo(f"Attention {schedule.message}: {payloads}")

        return self.success()


class CallablePrompter(Prompter):
    def __init__(self, final: bool = False) -> None:
        super().__init__(final)

    def prompt(self, payloads: PrompterPayloadCollection) -> PromptResult:
        hasCallable = False
        for payload in payloads.getUser():
            if callable(payload):
                payload()
                hasCallable = True
        return self.success() if hasCallable else PromptResult.Unsupported
