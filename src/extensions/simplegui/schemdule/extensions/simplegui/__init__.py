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

        auto_close_duration = max(
            min(int(schedule.duration.total_seconds() / 10), 60), 3)

        count = len(payloads)
        title = f"📣 {buildMessage(payloads)}"
        messages = [title, f"{count} payload{'' if count <= 1 else 's'}",
                    *(str(x) for x in payloads)]

        sg.popup_scrolled("\n".join(messages), title=title, auto_close=self.auto_close,
                          auto_close_duration=auto_close_duration,
                          keep_on_top=True, background_color='white', text_color='black')

        return self.success()
