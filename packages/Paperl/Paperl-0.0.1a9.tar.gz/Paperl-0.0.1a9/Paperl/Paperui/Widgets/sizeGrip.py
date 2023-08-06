from Paperl.Paperui.Widgets.widget import Widget


class SizeGrip(Widget):
    def __init__(self, parent: Widget):
        self.build(parent.Me)

    def build(self, parent):
        from tkinter.ttk import Sizegrip
        self.Me = Sizegrip(parent)
