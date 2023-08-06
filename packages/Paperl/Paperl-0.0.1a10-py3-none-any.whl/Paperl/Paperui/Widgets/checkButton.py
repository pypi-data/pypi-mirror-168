from Paperl.Paperui.Widgets.widget import Widget
from Paperl.Paperui.Widgets.button import Button
from Paperl.Paperui.Widgets.booleanVar import BooleanVar


class CheckButton(Button):
    def __init__(self, parent: Widget, text: str = "", falseVar=0, trueVar=1):
        self.build(parent.Me, text=text, falseVar=falseVar, trueVar=trueVar)

    def build(self, parent: Widget, text: str = "", falseVar=0, trueVar=1):
        from tkinter.ttk import Checkbutton
        self.Var = BooleanVar()
        self.Var.setValue(0)
        self.Me = Checkbutton(parent, text=text, variable=self.Var.Me, offvalue=falseVar, onvalue=trueVar)

    def inVoke(self):
        self.Me.invoke()

    def setValue(self, value: bool):
        self.Var.setValue(value)

    def getValue(self):
        return self.Var.getValue()