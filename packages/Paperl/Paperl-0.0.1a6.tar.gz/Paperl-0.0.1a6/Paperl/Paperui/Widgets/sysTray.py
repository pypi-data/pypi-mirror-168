from Paperl.Paperc import prWarring


class Systray(object):
    def __init__(self, master):
        self.build(master.Me)

    def build(self, master):
        try:
            from tkdev4.devtcl import DevTray
        except:
            prError("tkDev4 -> tkdev4 needs to be installed")
        else:
            try:
                self.Me = DevTray(master)
            except:
                prWarring("tkdev4 -> Parameter error")