from Paperl.Paperui.Widgets.widget import Widget


class Frame(Widget):
    def __init__(self, parent: Widget):
        self.build(parent.Me)

    def build(self, parent: Widget):
        from tkinter.ttk import Frame
        self.Me = Frame(parent)