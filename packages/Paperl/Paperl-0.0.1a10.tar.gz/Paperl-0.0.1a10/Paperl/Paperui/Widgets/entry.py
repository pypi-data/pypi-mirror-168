from Paperl.Paperui.Widgets.widget import Widget


class Entry(Widget):
    def __init__(self, parent: Widget, text: str = ""):
        self.build(parent.Me, text)

    def build(self, parent: Widget, text: str = ""):
        from tkinter.ttk import Entry
        from tkinter import StringVar
        self.Var = StringVar()
        self.Var.set(text)
        self.Me = Entry(parent, textvariable=text)

    def setText(self, text: str):
        self.Var.set(text)

    def getText(self):
        return self.Var.get()
