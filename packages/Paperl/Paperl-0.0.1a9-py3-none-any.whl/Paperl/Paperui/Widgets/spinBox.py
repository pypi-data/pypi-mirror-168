from Paperl.Paperui.Widgets.widget import Widget


class SpinBox(Widget):
    def __init__(self, parent: Widget, values: list = [""], startValue: float = 0, endValue: float = 10):
        self.build(parent.Me, values, startValue, endValue)

    def build(self, parent, values: list = None, startValue=0, endValue: float = 10):
        from tkinter.ttk import Spinbox
        self.Me = Spinbox(parent, values=values, from_=startValue, to=endValue)
