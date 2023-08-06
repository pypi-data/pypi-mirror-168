from Paperl.Paperui.Widgets.widget import Widget
from Paperl.Paperui.Widgets.stringsVar import StringsVar


class OptionMenu(Widget):
    def __init__(self, parent: Widget, defaultValue=None, valueList=[""]):
        self.build(parent.Me, defaultValue, valueList)

    def build(self, parent: Widget, defaultValue: str = None, valueList=[""]):
        from tkinter.ttk import OptionMenu
        self.Var = StringsVar()
        self.Me = OptionMenu(parent, self.Var.Me, defaultValue, *valueList)

    def setList(self, defaultValue=None, valueList=[""]):
        self.Me.set_menu(defaultValue, *valueList)

    def setMenu(self, defaultValue=None, valueList=[""]):
        self.Me.set_menu(defaultValue, *valueList)

    def setValue(self, value: str):
        self.Var.setValue(value)

    def getValue(self):
        return self.Var.getValue()
