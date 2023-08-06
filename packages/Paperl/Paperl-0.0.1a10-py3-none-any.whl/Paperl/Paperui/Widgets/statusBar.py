from Paperl.Paperui.Widgets.widget import Widget


class StatusBar(Widget):
    def __init__(self, parent: Widget):
        self.build(parent.Me)

    def build(self, parent):
        from tkdev4 import DevStatusBar
        self.Me = Sizegrip(parent)
