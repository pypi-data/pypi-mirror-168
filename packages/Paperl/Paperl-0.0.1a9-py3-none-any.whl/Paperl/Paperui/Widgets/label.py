from Paperl.Paperui.Widgets.widget import Widget


class Label(Widget):
    def __init__(self, parent: Widget, text: str = ""):
        self.build(parent.Me, text)

    def build(self, parent: Widget, text: str = ""):
        from tkinter.ttk import Label
        self.Me = Label(parent, text=text)
