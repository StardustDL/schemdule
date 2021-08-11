import PySimpleGUI as sg
from typing import Any
from schemdule.prompters import Prompter, PromptResult, PrompterPayloadCollection, getMessage

__version__ = "0.0.8"


class MessageBoxPrompter(Prompter):
    def __init__(self, auto_close: bool = False, final: bool = False) -> None:
        super().__init__(final)
        self.auto_close = auto_close

    def prompt(self, payloads: PrompterPayloadCollection) -> PromptResult:
        schedule = payloads.getSchedule()

        auto_close_duration = max(int(schedule.duration.total_seconds()), 3)

        sg.popup_scrolled(str(payloads), title=f"Attention {getMessage(payloads)}", auto_close=self.auto_close,
                          auto_close_duration=auto_close_duration,
                          keep_on_top=True, background_color='white', text_color='black')

        return self.success()
