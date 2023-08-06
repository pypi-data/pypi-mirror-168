from Paperl.Paperui.Widgets.widget import Widget


class Group(Widget):
    def __init__(self, parent: Widget, label: str = "", widget: Widget = None, anchor: str = "nw"):
        self.build(parent.Me, label, widget, anchor)

    def build(self, parent: Widget, label: str = "", widget: Widget = None, anchor: str = "nw"):
        from tkinter.ttk import Labelframe
        if widget is None:
            self.Me = Labelframe(parent, text=label)
        else:
            self.Me = Labelframe(parent, labelwidget=widget.Me, labelanchor=anchor)

    def setWidget(self, widget: Widget = None, anchor: str = "nw"):
        self.Me.configure(labelwidget=widget, labelanchor=anchor)