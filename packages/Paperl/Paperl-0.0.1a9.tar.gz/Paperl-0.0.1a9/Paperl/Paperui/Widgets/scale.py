from Paperl.Paperui.Widgets.widget import Widget


class Scale(Widget):
    def __init__(self, parent: Widget, startValue: float = 0, endValue: float = 100, value: float = 0, length: int = 100, orient="horizontal"):
        self.build(parent.Me, startValue, endValue, value, length, orient)

    def build(self, parent: Widget, startValue: float = 0, endValue: float = 100, value: float = 0, length: int = 100, orient="horizontal"):
        from tkinter.ttk import Scale
        self.Me = Scale(parent, from_=startValue, to=endValue, length=length, value=value, orient=orient)

    def onCommand(self, eventFunc: None = ...):
        self.Me.configure(command=eventFunc)

    def setOrient(self, orient):
        self.Me.configure(orient=orient)

    def getOrient(self):
        return self.Me.cget("orient")

    def setStartValue(self, startValue: float):
        self.Me.configure(from_=startValue)

    def getStartValue(self):
        return self.Me.cget("from_")

    def setEndValue(self, endValue: float):
        self.Me.configure(to=endValue)

    def getEndValue(self):
        return self.Me.cget("to")

    def setLength(self, length):
        self.Me.configure(length=length)

    def getLength(self):
        return self.Me.cget("length")

    def setValue(self, value):
        self.Me.configure(value=value)

    def getValue(self):
        return self.Me.cget("valur")