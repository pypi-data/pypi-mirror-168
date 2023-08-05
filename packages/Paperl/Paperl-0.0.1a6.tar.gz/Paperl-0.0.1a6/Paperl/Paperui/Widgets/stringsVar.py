class StringsVar(object):
    def __init__(self):
        self.build()

    def build(self):
        from tkinter import StringVar
        self.Me = StringVar()

    def setValue(self, value):
        self.Me.set(value)

    def getValue(self):
        return self.Me.get()