from Paperl.Paperui.Widgets.eventHandle import EventHandle
from Paperl.Paperc import prError, prDebugging, prWarring, prSuccess


class Widget(EventHandle):

    __name__ = "Widget"

    def __init__(self):
        super().__init__()

    def upDate(self):
        self.Me.update()

    def build(self):
        from tkinter import Widget
        try:
            self.Me = Widget()
        except:
            pass
        prDebugging("Widget -> Create")

    def destroy(self):
        self.Me.destroy()

    def setState(self, state):
        from tkinter import TclError
        try:
            self.Me.configure(state=state)
        except TclError:
            prError("Widget -> State -> This property is not supported or this value is not supported")

    def tkCall(self, __command, *args):
        try:
            self.Me.tk.call(__command, args)
        except:
            prError("Widget -> Tcl -> Error")

    def useDpi(self):
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
            ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
            self.Me.tk.call('tk', 'scaling', ScaleFactor / 75)
        except:
            prError("Widget -> Tcl -> Dpi -> The system does not support DPI")

    def setBackground(self, color):
        from tkinter import TclError
        try:
            self.Me.configure(background=color)
        except TclError:
            prError("Widget -> Background -> This property is not supported or this value is not supported")

    def setText(self, text: str):
        from tkinter import TclError
        try:
            self.Me.configure(text=text)
        except TclError:
            prError("Widget -> Text -> This property is not supported or this value is not supported")

    def getText(self):
        from tkinter import TclError
        try:
            return self.Me.cget("text")
        except TclError:
            prError("Widget -> Text -> This property is not supported or this value is not supported")

    def setForeground(self, color):
        from tkinter import TclError
        try:
            self.Me.configure(foreground=color)
        except TclError:
            prError("Widget -> Foreground -> This property is not supported or this value is not supported")

    def getSize(self):
        return self.Me.winfo_width(), self.Me.winfo_height()

    def getId(self):
        return self.Me.winfo_id()

    def gethWnd(self):
        try:
            from win32gui import GetParent
        except:
            prWarring("PyWin32 -> Check -> Not Installed")
            return None
        else:
            prSuccess("PyWin32 -> Check -> Installed")
            return GetParent(self.getId())

    def getSizeWidth(self) -> int:
        return self.Me.winfo_width()

    def getSizeWidth(self) -> int:
        return self.Me.winfo_height()

    def getPosition(self):
        return self.Me.winfo_x(), self.Me.winfo_y()

    def getPositionX(self) -> int:
        return self.Me.winfo_x()

    def getPositionY(self) -> int:
        return self.Me.winfo_y()

    def buttonUseDafaultStyle(self):
        self.Me.configure(style="TButton")

    def buttonUseSunValleyAccentStyle(self):
        try:
            self.Me.configure(style="Accent.TButton")
        except:
            prWarring(
                "Widget -> Use Accent Style -> Please use the SunValley theme"
            )

    def buttonUseSunValleyToggleStyle(self):
        try:
            self.Me.configure(style="Toggle.TButton")
        except:
            prWarring(
                "Widget -> Use Toggle Style -> Please use the SunValley theme"
            )

    def checkButtonUseSunValleySwichStyle(self):
        try:
            self.Me.configure(style="Switch.TCheckbutton")
        except:
            prWarring(
                "Widget -> Use Swich Style -> Please use the SunValley theme"
            )

    def setStyle(self, style):
        try:
            self.Me.configure(style=style)
        except:
            prWarring(
                "Widget -> Set Style -> Cannot"
            )

    def pack(self, paddingX: int = 0, paddingY: int = 0,
             marginX: int = 0, marginY: int = 0,
             fillType="none", expandType="no", sideType="top", anchorType="n"):
        try:
            self.Me.pack(ipadx=paddingX, ipady=paddingY, padx=marginX, pady=marginY,
                         fill=fillType, expand=expandType, side=sideType, anchor=anchorType)
        except:
            prError(
                "Widget -> Pack -> This component does not support this method or the value is filled in incorrectly"
            )

    def packForget(self):
        try:
            self.Me.pack_forget()
        except:
            prError(
                "Widget -> Pack Forget -> This component does not support this method or the value is filled in incorrectly"
            )

    def place(self, x: int = None, y: int = None, width: int = None, height: int = None, anchorType="center"):
        try:
            self.Me.place(x=x, y=y, width=width, height=height, anchor=anchorType)
        except:
            prError(
                "Widget -> Place -> This component does not support this method or the value is filled in incorrectly"
            )

    def placeForget(self):
        try:
            self.Me.place_forget()
        except:
            prError(
                "Widget -> Place Forget -> This component does not support this method or the value is filled in incorrectly"
                    )

    def showToast(self, title: str = "",
                  message: str = "Message",
                  appName: str = "Python",
                  appIcon: str = "",
                  timeOut: int = 0):
        try:
            from tkdev4 import DevNotification
        except:
            prError("tkDev4 -> Check -> Not Installed")
        else:
            try:
                DevNotification(title, message, appName, appIcon, timeOut).show()
            except:
                prError("Plyer -> Check -> Not Installed")