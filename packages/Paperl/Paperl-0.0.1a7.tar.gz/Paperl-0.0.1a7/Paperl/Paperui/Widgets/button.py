from Paperl.Paperui.Widgets.widget import Widget


class Button(Widget):
    def __init__(self, parent: Widget, text: str = ""):
        self.build(parent.Me, text)

    def build(self, parent, text: str):
        from tkinter.ttk import Button
        self.Me = Button(parent, text=text)

    def onCommand(self, eventFunc: None = ...):
        self.Me.configure(command=eventFunc)