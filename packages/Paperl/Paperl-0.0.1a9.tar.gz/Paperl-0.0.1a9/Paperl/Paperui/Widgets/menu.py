from Paperl.Paperui.Widgets.widget import Widget


class Menu(Widget):
    def __init__(self, parent: Widget = None, title: str = ""):
        if parent is None:
            Parent = None
        else:
            Parent = parent.Me
        self.build(Parent, title)

    def build(self, parent: Widget, title: str = ""):
        from tkinter import Menu
        self.Me = Menu(parent, title=title, border=0)
        self.setTearOff(False)

    def addCommand(self, label: str = "", state="normal",):
        self.Me.add_command(label=label, state=state)

    def onTearOff(self, eventFunc):
        self.Me.configure(tearoffcommand=eventFunc)

    def addMenu(self, menu: Widget, label: str = "", state="normal"):
        self.Me.add_cascade(label=label, state=state, menu=menu.Me)