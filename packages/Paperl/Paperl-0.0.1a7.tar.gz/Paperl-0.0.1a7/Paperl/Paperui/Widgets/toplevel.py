from Paperl.Paperui.Widgets.window import Window
from Paperl.Paperc import prDebugging, prError, prSuccess


class Toplevel(Window):
    __name__ = "Toplevel"

    def __init__(self, parent: Window = None):
        """
        顶级窗口组件，可以直接使用

        ------------------------

        示例

        from Paperl import *

        Application = Application()

        Window = Window()

        Toplevel = Toplevel()

        Application.run(Window)

        """
        if parent is None:
            self.build(None)
        else:
            self.build(parent.Me)
        self.init()
        try:
            from tkdev4 import DevManage
        except:
            pass
        else:
            try:
                self.windows_manage = DevManage(self.Me)
            except:
                pass
        self.setSystemBackdropNone()

    def build(self, parent) -> None:
        from tkinter import Toplevel
        self.Me = Toplevel(parent)
        prDebugging("Toplevel -> Build")
