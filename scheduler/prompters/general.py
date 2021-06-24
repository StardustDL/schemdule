import tkinter
import tkinter.messagebox

from . import Prompter


class TkinterPrompter(Prompter):
    def prompt(self, message: str) -> None:
        top = tkinter.Tk()
        top.withdraw()
        tkinter.messagebox.showinfo("Attention", message)
        top.destroy()
