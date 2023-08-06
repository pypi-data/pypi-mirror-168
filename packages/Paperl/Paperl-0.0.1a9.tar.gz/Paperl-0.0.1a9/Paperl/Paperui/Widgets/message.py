from Paperl.Paperui.Widgets.widget import Widget


class Message(Widget):
    def __init__(self, parent: Widget, text: str = ""):
        self.build(parent.Me, text)

    def build(self, parent: Widget, text: str = ""):
        from tkinter import Message
        self.Me = Message(parent, text=text, anchor="nw")
