from Paperl.Paperui.Widgets.window import Window
from Paperl.Paperc import prError, prSuccess


class Tooltip(Window):
    def __init__(self, parent, parentWindow, message: str = "", waitTime: int = 1000,
                 hasBorder: bool = True,
                 padding: int = 3,
                 sideType="center",
                 height: int = 40,
                 width=None,
                 cursor: bool = False,
                 background: str = "#ffffff",
                 foreground: str = "#000000"):
        self.build(parent.Me, parentWindow.Me, message, waitTime)

    def build(self, parent, parentWindow, message: str = "", waitTime: int = 1000,
              hasBorder: bool = True,
              padding: int = 3,
              sideType="center",
              height: int = 40,
              width=None,
              cursor: bool = False,
              background: str = "#ffffff",
              foreground: str = "#000000") -> None:
        try:
            from tkdev4 import DevTooltip
        except:
            pass
        else:
            try:
                self.Me = DevTooltip(widget=parent, window=parentWindow, message=message, after=waitTime, border=hasBorder,
                                     padding=padding, side=sideType, height=height, width=width, cursor=cursor,
                                     background=background, foreground=foreground)
            except:
                prError("ToolTip -> Creante -> Error")


class TooltipEx(object):
    def __init__(self, parent, message: str = "", waitTime: float = 0.5):
        self.build(parent.Me, message, waitTime)

    def build(self, parent, message: str = "", waitTime: float = 0.5):
        try:
            from tktooltip import ToolTip
        except:
            prError("tkinter-tooltip -> Check -> Not Installed")
        else:
            prSuccess("tkinter-tooltip -> Check -> Installed")
            self.Me = ToolTip(parent, message, waitTime)