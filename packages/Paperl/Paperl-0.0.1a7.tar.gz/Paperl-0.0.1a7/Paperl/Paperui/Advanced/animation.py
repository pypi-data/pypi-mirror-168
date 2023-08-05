from Paperl.Paperui.Widgets.widget import Widget


class Animation(object):
    def __init__(self, control: Widget):
        self.Me = control

    def gradualMovement(self, action, move: int = 100, time: float = 0.01):
        try:
            def motion():
                try:
                    from time import sleep
                    for c in range(move):
                        sleep(time)
                        if action == "left-right":
                            self.Me.place(x=self.Me.getPositionX() + 1, y=self.Me.getPositionY())
                        elif action == "right-left":
                            self.Me.place(x=self.Me.getPositionX() - 1, y=self.Me.getPositionY())
                        elif action == "top-bottom":
                            self.Me.place(x=self.Me.getPositionX(), y=self.Me.getPositionY() + 1)
                        elif action == "bottom-top":
                            self.Me.place(x=self.Me.getPositionX(), y=self.Me.getPositionY() - 1)
                        self.Me.upDate()
                except:
                    pass
            self.Me.waitEvent(10, motion)
        except:
            pass

    def gradualWindowShow(self, number: int = 100, time: float = 0.01):
        self.Me.setAlpha(0.0)
        from time import sleep
        for num in range(number):
            sleep(time)
            self.Me.setAlpha(num/100)
            self.Me.upDate()
        self.Me.setAlpha(1.0)

    def gradualWindowHide(self, number: int = 100, time: float = 0.01):
        self.Me.setAlpha(1.0)
        from time import sleep
        for num in range(number):
            sleep(time)
            self.Me.setAlpha(1-num/100)
            self.Me.upDate()
        self.Me.setAlpha(0.0)
