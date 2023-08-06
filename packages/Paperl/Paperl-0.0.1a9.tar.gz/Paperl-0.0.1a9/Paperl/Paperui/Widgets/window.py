from Paperl.Paperui.Widgets.widget import Widget
from Paperl.Paperui.Widgets.windowDevelop import WindowsDev
from Paperl.Paperui.Widgets.themes import Themes
from Paperl.Paperc import prDebugging, prError, prSuccess, prWarring
from functools import singledispatch
from typing import Literal


class Window(Widget, WindowsDev, Themes):
    __name__ = "Window"

    def __init__(self):
        """
        窗口组件，可以配合Application一起使用，也可以直接使用

        ------------------------

        示例

        from Paperl import *

        Application = Application()

        Window = Window()

        Application.run(Window)

        ------------------------

        示例

        from Paperl import *

        Window = Window()

        Window.run()

        """

        self.build()
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

    def build(self) -> None:
        from tkinter import Tk
        self.Me = Tk()
        prDebugging("Window -> Build")

    def bindEventEx(self, eventName=None, eventFunc: None = ...):
        self.Me.protocol(eventName, eventFunc)

    def jumpTaskBar(self):
        from ctypes import windll

        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080

        style = windll.user32.GetWindowLongW(self.gethWnd(), GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(self.gethWnd(), GWL_EXSTYLE, style)
        # re-assert the new window style
        self.hide()
        self.waitEvent(10, lambda: self.show())

    def createHeaderBar(self, border: bool = True, sizeGrip: bool = False):
        from Paperl.Paperui.Widgets.headerBar import HeaderBarEx
        HeaderBar = HeaderBarEx(self, self, border=border)
        HeaderBar.addTitleBar()
        HeaderBar.setTitle(self.getTitle())
        HeaderBar.useDoubleLeftMaximize()
        HeaderBar.useDoubleMiddleClose()
        if sizeGrip:
            HeaderBar.addSizeGrip()
        HeaderBar.show()
        return HeaderBar

    def canResize(self, width: bool = None, height: bool = None):
        self.Me.resizable(width, height)

    def setMinsize(self, width: int = None, height: int = None):
        self.Me.minsize(width, height)

    def setMaxsize(self, width: int = None, height: int = None):
        self.Me.maxsize(width, height)

    def setWidgetIsWindow(self, widget):
        self.Me.manage(widget.Me)

    def minimize(self):
        self.Me.iconify()

    def normal(self):
        self.Me.deiconify()

    def onSaveYourself(self, eventFunc: None = ...):
        self.bindEventEx("WM_SAVE_YOURSELF", eventFunc)

    def onDeleteWindow(self, eventFunc: None = ...):
        self.bindEventEx("WM_DELETE_WINDOW", eventFunc)

    def setPalette(self, *args, **kwargs):
        self.Me.tk_setPalette(args, kwargs)

    def setAttribute(self, attributeName, attributeValue=True):
        try:
            self.Me.attributes(attributeName, attributeValue)
        except:
            prWarring("Window -> SetAttribute -> The system does not support this property")

    def popup(self, x, y):
        self.setPosition(x, y)

    def setAlpha(self, value: float = 1.0):
        self.setAttribute("-alpha", value)

    def setModified(self, bool: bool = True):
        self.setAttribute("-modified", bool)

    def setTransparent(self, bool: bool = True):
        self.setAttribute("-transparent", bool)

    def setTopping(self, isTop: bool = True):
        self.setAttribute("-topmost", isTop)

    def setToolWindow(self, isToolWindow: bool = True):
        self.setAttribute("-toolwindow", isToolWindow)

    def bell(self):
        self.Me.bell()

    def init(self) -> None:
        self.setEmptyIcon()
        self.setBackground("#ffffff")
        self.setTitle("Paperl")
        self.setSize(250, 250)

    def setIcon(self, image):
        self.Me.iconbitmap(image)

    def setEmptyIcon(self):
        try:
            from tkdev4.devicon import Icon_Empty
            self.emptyIcon = Icon_Empty
            self.setIcon(Icon_Empty)
        except:
            pass

    def setFolderIcon(self):
        try:
            from tkdev4.devicon import Icon_Folder
            self.folderIcon = Icon_Folder
            self.setIcon(Icon_Folder)
        except:
            pass

    def setPythonIcon(self):
        try:
            from sys import executable
            from os.path import exists, split
            icon = split(executable)[0] + "\\DLLs\\py.ico"
            if exists(icon):
                self.pythonIcon = icon
                self.setIcon(icon)
        except:
            pass

    def setPythoncIcon(self):
        try:
            from sys import executable
            from os.path import exists, split
            icon = split(executable)[0] + "\\DLLs\\pyc.ico"
            if exists(icon):
                self.pythoncIcon = icon
                self.setIcon(icon)
        except:
            pass

    def setPythondIcon(self):
        try:
            from sys import executable
            from os.path import exists, split
            icon = split(executable)[0] + "\\DLLs\\pyd.ico"
            if exists(icon):
                self.pythondIcon = icon
                self.setIcon(icon)
        except:
            pass

    def setIdleIcon(self):
        try:
            from sys import executable
            from os.path import exists, split
            icon = split(executable)[0] + "\\Lib\\idlelib\\Icons\\idle.ico"
            if exists(icon):
                self.pythondIcon = icon
                self.setIcon(icon)
        except:
            pass

    def setText(self, text: str):
        from tkinter import TclError
        try:
            self.setTitle(text)
        except TclError:
            prError("Window -> Text -> This property is not supported or this value is not supported")

    def getText(self):
        from tkinter import TclError
        try:
            return self.getTitle()
        except TclError:
            prError("Window -> Text -> This property is not supported or this value is not supported")

    def setTitle(self, title: str) -> None:
        self.Me.title(title)

    def getTitle(self) -> str:
        return self.Me.title()

    def setGeometry(self, width: int, height: int, x: int, y: int) -> None:
        self.Me.geometry(f"{str(width)}x{str(height)}+{str(x)}+{str(y)}")

    def getGeometry(self):
        return self.getSize(), self.getPosition()

    def setSize(self, width: int, height: int) -> None:
        self.Me.geometry(f"{str(width)}x{str(height)}")

    def setPosition(self, x: int, y: int) -> None:
        self.Me.geometry(f"+{str(x)}+{str(y)}")

    def maximizeBox(self):
        try:
            self.windows_manage.add_window_maximizebox()
        except:
            pass

    def minimizeBox(self):
        try:
            self.windows_manage.add_window_minimizebox()
        except:
            pass

    def systemMenu(self):
        try:
            self.windows_manage.add_window_sysmenu()
        except:
            pass

    def showWindow(self, nCmdShow):
        try:
            from win32gui import ShowWindow
        except:
            pass
        else:
            ShowWindow(self.gethWnd(), nCmdShow)

    def showMaximizeEx(self):
        try:
            from win32con import SW_SHOWMAXIMIZED
        except:
            pass
        else:
            self.showWindow(SW_SHOWMAXIMIZED)

    def showMaximizeLx(self):
        self.setState("zoomed")

    def showMinimizeEx(self):
        try:
            from win32con import SW_SHOWMINIMIZED
        except:
            pass
        else:
            self.showWindow(SW_SHOWMINIMIZED)

    def showNormalEx(self):
        try:
            from win32con import SW_SHOWNORMAL
        except:
            pass
        else:
            self.showWindow(SW_SHOWNORMAL)

    def hideEx(self):
        try:
            from win32con import SW_HIDE
        except:
            pass
        else:
            self.showWindow(SW_HIDE)

    def show(self):
        self.Me.deiconify()

    def hide(self):
        self.Me.withdraw()

    def showEx(self):
        try:
            from win32con import SW_SHOW
        except:
            pass
        else:
            self.showWindow(SW_SHOW)

    def removeCaption(self, isRemove: bool = True):
        self.Me.overrideredirect(isRemove)

    def removeCaptionEx(self):
        try:
            self.windows_manage.add_window_titlebar()
        except:
            pass

    def hideTitleBar(self):
        self.removeCaption()

    def hideTitleBarBorderEx(self):
        self.windows_manage.add_window_resize_border_frame()

    def hideTitleBarEx(self):
        self.removeCaptionEx()

    def mainLoop(self) -> None:
        prDebugging("Window -> MainLoop")
        try:
            self.Me.mainloop()
        except:
            prError("Window -> MainLoop -> Error")
        prDebugging("Window -> Quit")

    def run(self) -> None:
        prDebugging("Window -> Run")
        try:
            self.Me.mainloop()
        except:
            prError("Window -> Run -> Error")
        prDebugging("Window -> Quit")
