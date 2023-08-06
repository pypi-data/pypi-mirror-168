from Paperl.Paperui.Widgets.frame import Frame
from Paperl.Paperui.Widgets.widget import Widget


class DragFrame(Frame):
    def __init__(self, parent: Widget):
        self.build(parent.Me)

    def build(self, parent: Widget):
        from tkinter.ttk import Frame
        self.Me = Frame(parent)
        try:
            from tkdev4 import DevManage
        except:
            pass
        else:
            DevManage(self.Me).send_message_move_window(parent)