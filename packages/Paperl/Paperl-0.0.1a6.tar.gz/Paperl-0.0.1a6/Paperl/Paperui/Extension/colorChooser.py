from Paperl.Paperui.Widgets.widget import Widget


class ColorChooserDialog(object):
    def __init__(self):
        self.build()

    def build(self):
        pass

    def getColor(self):
        from tkinter.colorchooser import askcolor
        return askcolor()

    def getColorRgb(self):
        return self.getColor()[0]

    def getColorHex(self):
        return self.getColor()[1]

def getColor():
    return ColorChooserDialog().getColor()

def getColorRgb():
    return ColorChooserDialog().getColorRgb()

def getColorHex():
    return ColorChooserDialog().getColorHex()