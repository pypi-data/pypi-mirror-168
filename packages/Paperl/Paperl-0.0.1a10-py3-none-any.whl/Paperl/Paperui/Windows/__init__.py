def getText(widget):
    try:
        from win32gui import GetWindowText
    except:
        pass
    else:
        try:
            return GetWindowText(widget.gethWnd())
        except:
            pass

def setText(widget, text: str = ""):
    try:
        from win32gui import SetWindowText
    except:
        pass
    else:
        try:
            return SetWindowText(widget.gethWnd(), text)
        except:
            pass