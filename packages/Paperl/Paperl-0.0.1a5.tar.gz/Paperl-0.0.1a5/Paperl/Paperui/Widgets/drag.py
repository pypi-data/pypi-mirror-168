class Drag(object):
    def __init__(self, parentWidget, dragWidget, dragX: bool = True, dragY: bool = True, isWindow: bool = False):
        self.build(parentWidget, dragWidget, dragX, dragY, isWindow)

    def build(self, parentWidget, dragWidget, dragX: bool = True, dragY: bool = True, isWindow: bool = False):
        from tkdev4 import DevDrag
        self.Me = DevDrag(widget=parentWidget.Me, dragwidget=dragWidget.Me, x=dragX, y=dragY, iswindow=isWindow)