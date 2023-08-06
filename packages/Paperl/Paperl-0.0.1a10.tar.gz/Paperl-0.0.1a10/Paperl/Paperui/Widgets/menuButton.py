from Paperl.Paperui.Widgets.widget import Widget


class MenuButton(Widget):
    def __init__(self, parent: Widget, text: str = "", menu: Widget = None):
        if menu is None:
            Menu = None
        else:
            Menu = menu.Me
        self.build(parent.Me, text, menu)

    def build(self, parent: Widget, text: str = "", menu: Widget = None):
        from tkinter.ttk import Menubutton
        self.Me = Menubutton(parent, text=text, menu=menu)
