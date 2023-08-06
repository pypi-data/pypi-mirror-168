from Paperl.Paperui.Widgets.widget import Widget


class ResizeHandleIx(object):
    def __init__(self, parent: Widget, handleSize=8, gridded=1, minimizeWidth=50, minimizeHeight=50):
        self.build(parent.Me, handleSize=handleSize, gridded=gridded, minimizeWidth=minimizeWidth, minimizeHeight=minimizeHeight)

    def build(self, parent: Widget, handleSize=8, gridded=1, minimizeWidth=50, minimizeHeight=50):
        from tkinter.tix import ResizeHandle
        self.Me = ResizeHandle(parent, handlesize=handleSize, gridded=gridded, minwidth=minimizeWidth, minheight=minimizeHeight)

    def attach(self, widget: Widget):
        self.Me.attach_widget(widget.Me)

    def detach(self, widget: Widget):
        self.Me.detach_widget(widget.Me)

    def show(self, widget: Widget):
        self.Me.show(widget)

    def hide(self, widget: Widget):
        self.Me.hide(widget)