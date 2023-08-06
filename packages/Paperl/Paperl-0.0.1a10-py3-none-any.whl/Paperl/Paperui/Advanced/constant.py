ANIMATION_LEFT_TO_RIGHT = "left-right"
ANIMATION_RIGHT_TO_LEFT = "right-left"
ANIMATION_TOP_TO_BOTTOM = "top-bottom"
ANIMATION_BOTTOM_TO_TOP = "bottom-top"

try:
    from win32con import AW_BLEND, AW_HIDE
    ANIMATION_WINDOWS_BLEND = AW_BLEND
    ANIMATION_WINDOWS_HIDE = AW_HIDE
except:
    pass