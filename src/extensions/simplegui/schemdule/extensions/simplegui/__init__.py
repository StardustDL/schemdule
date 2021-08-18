from datetime import timedelta
from typing import Any

import PySimpleGUI as sg
from schemdule.helpers import buildMessage
from schemdule.prompters import PayloadCollection, Prompter, PromptResult

__version__ = "0.0.11"


class MessageBoxPrompter(Prompter):
    def __init__(self, autoClose: bool, maxKeep: timedelta, final: bool = False) -> None:
        super().__init__(final)
        self.autoClose = autoClose
        self.maxKeep = maxKeep

    def prompt(self, payloads: PayloadCollection) -> PromptResult:
        schedule = payloads.getSchedule()

        auto_close_duration = int(max(
            min(schedule.duration.total_seconds() / 10, self.maxKeep.total_seconds()), 3))

        count = len(payloads)
        title = f"📣 {buildMessage(payloads)}"
        messages = [title, f"{count} payload{'' if count <= 1 else 's'}",
                    *(str(x) for x in payloads)]

        sg.popup_scrolled("\n".join(messages), title=title, auto_close=self.autoClose,
                          auto_close_duration=auto_close_duration,
                          keep_on_top=True, background_color='white', text_color='black')

        return self.success()
