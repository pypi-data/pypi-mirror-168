class BooleanVar(object):
    def __init__(self):
        self.build()

    def build(self):
        from tkinter import BooleanVar
        self.Me = BooleanVar()

    def setValue(self, value):
        self.Me.set(value)

    def getValue(self):
        return self.Me.get()