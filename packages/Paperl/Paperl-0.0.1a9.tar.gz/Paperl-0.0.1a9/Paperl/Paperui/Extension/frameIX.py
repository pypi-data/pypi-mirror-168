from Paperl.Paperui.Widgets.frame import Frame
from Paperl.Paperui.Widgets.widget import Widget


class FrameIx(Frame):
    def __init__(self, parent: Widget):
        self.build(parent.Me)

    def build(self, parent: Widget):
        from tkinter.tix import Frame
        self.Me = Frame(parent)
