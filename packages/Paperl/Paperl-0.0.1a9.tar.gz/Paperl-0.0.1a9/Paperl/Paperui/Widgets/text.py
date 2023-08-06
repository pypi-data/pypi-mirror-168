from Paperl.Paperui.Widgets.widget import Widget


class Text(Widget):
    def __init__(self, parent: Widget):
        self.build(parent.Me)

    def build(self, parent):
        from tkinter import Text
        self.Me = Text(parent)
        self.setFont("微软雅黑", 9)
        self.Me.configure(border=0)

    def insertText(self, index="1.0", text: str = ""):
        self.Me.insert(index, text)

    def getText(self, start="1.0", end="end"):
        return self.Me.get(start, end)

    def getTextAll(self):
        return self.getText("1.0", "end")

    def deleteText(self, start="1.0", end="end"):
        self.Me.delete(start, end)

    def deleteTextAll(self):
        self.deleteText("1.0", "end")

    def setText(self, text: str):
        self.deleteTextAll()
        self.insertText(index="1.0", text=text)
