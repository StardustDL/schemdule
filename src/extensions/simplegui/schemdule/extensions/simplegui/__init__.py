import PySimpleGUI as sg
from typing import Any
from schemdule.prompters import Prompter, PromptResult

__version__ = "0.0.7"


class MessageBoxPrompter(Prompter):
    def __init__(self, final: bool = False, auto_close: bool = False) -> None:
        super().__init__(final)
        self.auto_close = auto_close

    def prompt(self, message: str, payload: Any) -> Any:
        sg.popup_scrolled(str(payload), title=f"Attention {message}", auto_close=self.auto_close,
                          keep_on_top=True, background_color='white', text_color='black')

        return self.success()
