from Paperl.Paperui.Widgets.widget import Widget


class Balloon(Widget):
    def __init__(self, parent: Widget):
        self.build(parent.Me)

    def build(self, parent):
        try:
            from tkinter import tix
            self.Me = tix.Balloon(parent)
        except:
            pass

    def addWidget(self, widget: Widget, message: str = ""):
        self.Me.bind_widget(widget.Me, balloonmsg=message)