from Paperl.Paperc import prError


class Image(object):
    def __init__(self):
        self.build()

    def build(self):
        pass

    def setImageSvg(self, file):
        try:
            from tksvg import SvgImage
        except:
            prError("tkSvg -> Check -> Not Installed")
        else:
            self.Me = SvgImage(file=file)

    def setImage(self, file, height: int = None, width: int = None):
        from tkinter import PhotoImage
        if height is None and width is None:
            self.Me = PhotoImage(file=file)
        else:
            try:
                self.Me = PhotoImage(file=file, height=height, width=width)
            except:
                pass

    def export(self):
        try:
            return self.Me
        except:
            prError("Image -> export -> Error")