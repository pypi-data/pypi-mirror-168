from Paperl.Paperui.Widgets.dragFrame import DragFrame
from Paperl.Paperui.Widgets.widget import Widget
from Paperl.Paperui.Widgets.window import Window
from Paperl.Paperui.Widgets.label import Label
from Paperl.Paperui.Widgets.button import Button
from Paperl.Paperui.Widgets.sizeGrip import SizeGrip


class HeaderBarEx(DragFrame):
    def __init__(self, parent: Widget, window: Window, border: bool = True):
        super().__init__(parent)
        self.Window = window
        self.Window.setMinsize(100, 60)
        if border:
            self.Window.hideTitleBarEx()
        else:
            self.Window.hideTitleBar()

            try:
                self.Window.jumpTaskBar()
            except:
                pass

        self.Window.setExtendFrameIntoClientArea(0, 0, 0, 0)
        self.Title = Label(self)
        self.Close = Button(self)
        self.Max = Button(self)
        self.Min = Button(self)
        self.SizeGrip = SizeGrip(self.Window)
        self.isMin = False

    def maximize(self, event=None):
        if self.isMin:
            self.isMin = False

            self.Window.showNormalEx()
        else:
            self.isMin = True
            self.Window.showMaximizeEx()

    def setText(self, text: str):
        self.Window.setTitle(text)
        self.Title.setText(text)

    def setTitle(self, title: str):
        self.Window.setTitle(title)
        self.Title.setText(title)

    def addTitle(self, anchor="center"):
        self.Title.setFont("Microsoft YaHei UI", 9)
        self.Title.pack(sideType="left", anchorType=anchor, marginX=20, marginY=5)

    def addCloseButton(self, text: str = "×"):
        self.Close.setText(text)
        self.Close.onCommand(lambda: self.Window.destroy())
        self.Close.pack(sideType="right", fillType="y", marginX=10, marginY=5, paddingX=1)

    def addMinimizeButton(self, text: str = "–"):
        self.Min.setText(text)
        self.Min.onCommand(lambda: self.Window.showMinimizeEx())
        self.Min.pack(sideType="right", fillType="y", marginX=10, marginY=5, paddingX=1)

    def addMaximizeButton(self, text: str = "□"):
        self.Max.setText(text)
        self.Max.onCommand(self.maximize)
        self.Max.pack(sideType="right", fillType="y", marginX=10, marginY=5, paddingX=1)

    def useDoubleLeftMaximize(self):
        self.onButtonDoubleLeft(self.maximize)

    def useDoubleMiddleClose(self):
        self.onButtonDoubleMiddle(lambda event: self.Window.destroy())

    def addTitleBar(self):
        self.addCloseButton()
        self.addMaximizeButton()
        self.addMinimizeButton()
        self.addTitle()

    def useSunValley(self, theme="auto"):
        self.Window.useStyleSunValley(theme)
        self.Close.buttonUseSunValleyTitleBarCloseStyle()
        self.Max.buttonUseSunValleyTitleBarStyle()
        self.Min.buttonUseSunValleyTitleBarStyle()

    def addSizeGrip(self):
        self.SizeGrip.pack(sideType="bottom", anchorType="se", paddingX=5, paddingY=5)

    def show(self):
        self.pack(fillType="x", sideType="top")
