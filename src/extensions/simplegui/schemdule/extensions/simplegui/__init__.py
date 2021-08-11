from typing import Any

import PySimpleGUI as sg
from schemdule.helpers import buildMessage
from schemdule.prompters import PayloadCollection, Prompter, PromptResult

__version__ = "0.0.9"


class MessageBoxPrompter(Prompter):
    def __init__(self, auto_close: bool = False, final: bool = False) -> None:
        super().__init__(final)
        self.auto_close = auto_close

    def prompt(self, payloads: PayloadCollection) -> PromptResult:
        schedule = payloads.getSchedule()

        auto_close_duration = max(int(schedule.duration.total_seconds()), 3)

        count = len(payloads)
        messages = [f"{count} payload{'' if count <= 1 else 's'}",
                    *(str(x) for x in payloads)]

        sg.popup_scrolled("\n".join(messages), title=f"📣 {buildMessage(payloads)}", auto_close=self.auto_close,
                          auto_close_duration=auto_close_duration,
                          keep_on_top=True, background_color='white', text_color='black')

        return self.success()
