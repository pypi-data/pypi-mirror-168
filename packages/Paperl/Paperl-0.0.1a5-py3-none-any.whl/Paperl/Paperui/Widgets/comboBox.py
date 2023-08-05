from Paperl.Paperui.Widgets.widget import Widget


class ComboBox(Widget):
    def __init__(self, parent: Widget, values=[]):
        self.build(parent.Me, values)

    def build(self, parent: Widget, values=[]):
        from tkinter import ttk
        self.Me = ttk.Combobox(parent, values=values)

    def current(self, index):
        self.Me.current(index)

    def setReadonly(self):
        self.setState("readonly")

    def setValues(self, values):
        self.Me.configure(values=values)

    def getValues(self):
        return self.Me.cget("values")

    def setText(self, text: str):
        self.Me.set(text)

    def getText(self):
        return self.Me.get()