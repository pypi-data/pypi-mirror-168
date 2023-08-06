from Paperl.Paperui.Widgets.widget import Widget
from Paperl.Paperui.Widgets.toplevel import Toplevel


class PopupMenuEx(Toplevel):
    def __init__(self, parent: Widget):
        self.parent = parent
        self.build(parent.Me)

    def build(self, parent: Widget):
        from tkinter import Toplevel
        self.Me = Toplevel(parent)

        self.hide()
        self.removeCaptionEx()
        self.setRoundSmall()

        self.onFocusIn(lambda Evt: self.show())
        self.onFocusOut(lambda Evt: self.hide())

    def onCommand(self, eventName):
        self.bindEvent(eventName, self.popupMenu)

    def popupMenu(self, event):
        print("asda")
        self.setFocus()
        self.show()
        self.popup(event.x + self.parent.getPositionX(), event.y + self.parent.getPositionY() + 40)