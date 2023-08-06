from Paperl.Paperui.Widgets.widget import Widget


class ProgressBar(Widget):
    def __init__(self, parent: Widget, orient="horizontal", mode="determinate", length=100, value: float = 0, maxValue: float = 100):
        self.build(parent.Me, orient, mode, length, value, maxValue)

    def build(self, parent: Widget, orient, mode, length, value, maxValue):
        from tkinter.ttk import Progressbar
        self.Me = Progressbar(parent, orient=orient, mode=mode, length=length, value=value, maximum=maxValue)

    def setLength(self, length):
        self.Me.configure(length=length)

    def getLength(self):
        return self.Me.cget("length")

    def setOrient(self, orient):
        self.Me.configure(orient=orient)

    def getOrient(self):
        return self.Me.cget("orient")

    def setValue(self, value):
        self.Me.configure(value=value)

    def getValue(self):
        return self.Me.cget("value")

    def setMaxValue(self, value):
        self.Me.configure(maximum=value)

    def getMaxValue(self):
        return self.Me.cget("maximum")

    def startProgress(self, time: int = 50):
        self.Me.start(time)

    def stepProgress(self, value: float = 1.0):
        self.Me.step(value)

    def stopProgress(self):
        self.Me.stop()