from Paperl.Paperui.Widgets.toplevel import Toplevel
from Paperl.Paperui.Widgets.window import Window


class ChildWindowEx(Toplevel):
    def __init__(self, parent: Window):
        super().__init__(parent)
        self.embedEx(parent)