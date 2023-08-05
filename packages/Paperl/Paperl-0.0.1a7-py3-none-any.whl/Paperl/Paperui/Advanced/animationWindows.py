from Paperl.Paperui.Widgets.widget import Widget


class AnimationWindows(object):
    def __init__(self, parent: Widget, timeMs=200, flags=0x00080000):
        self.build(parent.gethWnd(), timeMs, flags)

    def build(self, parent: Widget, timeMs, flags):
        from ctypes import windll
        from ctypes import c_int
        self.Me = windll.user32.AnimateWindow(parent, timeMs, flags)
        return self.Me