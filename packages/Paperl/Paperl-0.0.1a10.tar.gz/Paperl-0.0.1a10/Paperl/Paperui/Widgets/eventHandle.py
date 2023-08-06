from Paperl.Paperui.Widgets.constant import *
from Paperl.Paperc import prDebugging, prError


class EventHandle(object):
    def __init__(self):
        self.build()

    def build(self):
        from tkinter import Widget
        try:
            self.Me = Widget()
        except:
            pass

    def waitEvent(self, eventTime: int, eventFunc: None = ...):
        try:
            self.Me.after(eventTime, eventFunc)
        except:
            prError("Widget -> Bind -> Please confirm whether the eventTime is correct or the eventFunc is wrong")

    def bindEvent(self, eventName=None, eventFunc: None = ...):
        try:
            self.Me.bind(eventName, eventFunc)
        except:
            prError("Widget -> Bind -> Please confirm whether the eventName is correct or the eventFunc is wrong")

    # Event Button

    def onButtonLeft(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onButtonLeft")
        self.bindEvent(EVENT_BUTTON1, eventFunc)

    def onButtonMiddle(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onButtonMiddle")
        self.bindEvent(EVENT_BUTTON2, eventFunc)

    def onButtonRight(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onButtonRight")
        self.bindEvent(EVENT_BUTTON3, eventFunc)

    def onButtonAll(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onButtonAll")
        self.bindEvent(EVENT_BUTTON_ALL, eventFunc)

    def onButtonPress(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onButtonPress")
        self.bindEvent(EVENT_BUTTON_PRESS, eventFunc)

    # Event Button Release

    def onButtonReleaseLeft(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onButtonReleaseLeft")
        self.bindEvent(EVENT_BUTTON1_RELEASE, eventFunc)

    def onButtonReleaseMiddle(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onButtonReleaseMiddle")
        self.bindEvent(EVENT_BUTTON2_RELEASE, eventFunc)

    def onButtonReleaseRight(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onButtonReleaseRight")
        self.bindEvent(EVENT_BUTTON3_RELEASE, eventFunc)

    def onButtonReleaseAll(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onButtonReleaseAll")
        self.bindEvent(EVENT_BUTTON_ALL_RELEASE, eventFunc)

    # Event Button Double

    def onButtonDoubleLeft(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onButtonDoubleLeft")
        self.bindEvent(EVENT_BUTTON1_DOUBLE, eventFunc)

    def onButtonDoubleMiddle(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onButtonDoubleMiddle")
        self.bindEvent(EVENT_BUTTON2_DOUBLE, eventFunc)

    def onButtonDoubleRight(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onButtonDoubleRight")
        self.bindEvent(EVENT_BUTTON3_DOUBLE, eventFunc)

    def onButtonDoubleAll(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onButtonDoubleAll")
        self.bindEvent(EVENT_BUTTON_ALL_DOUBLE, eventFunc)

    def onButtonDoublePress(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onButtonDoublePress")
        self.bindEvent(EVENT_BUTTON_PRESS_DOUBLE, eventFunc)

    # Event Button Triple

    def onButtonTripleLeft(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onButtonTripleLeft")
        self.bindEvent(EVENT_BUTTON1_TRIPLE, eventFunc)

    def onButtonTripleMiddle(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onButtonTripleMiddle")
        self.bindEvent(EVENT_BUTTON2_TRIPLE, eventFunc)

    def onButtonTripleRight(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onButtonTripleRight")
        self.bindEvent(EVENT_BUTTON3_TRIPLE, eventFunc)

    def onButtonTripleAll(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onButtonTripleAll")
        self.bindEvent(EVENT_BUTTON_ALL_TRIPLE, eventFunc)

    def onButtonTriplePress(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onButtonTriplePress")
        self.bindEvent(EVENT_BUTTON_PRESS_TRIPLE, eventFunc)

    # Event Widget

    def onDestroy(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onDestroy")
        self.bindEvent(EVENT_DESTROY, eventFunc)

    def onKey(self, key: str = "", eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onKey")
        self.bindEvent(f"<{key}>", eventFunc)

    def onEnter(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onEnter")
        self.bindEvent(EVENT_ENTER, eventFunc)

    def onLeave(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onLeave")
        self.bindEvent(EVENT_LEAVE, eventFunc)

    def onFocusIn(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onFocusIn")
        self.bindEvent(EVENT_FOCUS_IN, eventFunc)

    def onFocusOut(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onFocusOut")
        self.bindEvent(EVENT_FOCUS_OUT, eventFunc)

    def onConfigure(self, eventFunc: None = ...):
        prDebugging("Widget -> Bind -> onConfigure")
        self.bindEvent(EVENT_CONFIGURE, eventFunc)
