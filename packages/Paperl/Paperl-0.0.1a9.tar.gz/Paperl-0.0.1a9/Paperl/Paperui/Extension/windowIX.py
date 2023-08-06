from Paperl.Paperui.Widgets.window import Window
from Paperl.Paperc import prDebugging


class WindowIx(Window):
    def __init__(self):
        super().__init__()

    def build(self) -> None:
        from tkinter import tix
        self.Me = tix.Tk()
        prDebugging("WindowIX -> Build")
