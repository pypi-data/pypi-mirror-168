from typing import Literal
from win32 import win32api
from win32.lib import win32con

class ScreenCoordinates:
    def __init__(self, x: int, y: int, *, do_round: bool = True) -> None:
        self.x = int(round(x, 0))
        self.y = int(round(y, 0))

        if do_round: self.unrounded = ScreenCoordinates(x, y, do_round=False)
        else:
            self.x = int(x)
            self.y = int(y)
            self.unrounded = self

    @staticmethod
    def center(*, monitor: int = 0):
        monitors = win32api.EnumDisplayMonitors()
        if monitor > len(monitors) - 1 or monitor < 0:
            raise IndexError("Invalid monitor.")
        dimensions = monitors[monitor][2]
        _, _, x, y = dimensions
        return ScreenCoordinates(x / 2, y / 2)
    
    def get_unrounded(self):
        return self.unrounded
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def __tuple__(self) -> tuple:
        return self.x, self.y
    
    def __dict__(self) -> dict:
        return {"x": self.x, "y": self.y}
    
    def __str__(self) -> str:
        return f"{self.x}:{self.y}"

class MouseButtons:
    def __init__(self, *, down: Literal, up: Literal, key: Literal) -> None:
        self.down = down
        self.up = up
        self.key = key
    
    def __eq__(self, __o: object) -> bool:
        return self.key == __o.key

    @staticmethod
    def left():
        return MouseButtons(
            down=win32con.WM_LBUTTONDOWN,
            up=win32con.WM_LBUTTONUP,
            key=win32con.MK_LBUTTON
        )

    @staticmethod
    def right():
        return MouseButtons(
            down=win32con.WM_RBUTTONDOWN,
            up=win32con.WM_RBUTTONUP,
            key=win32con.MK_RBUTTON
        )

    @staticmethod
    def middle():
        return MouseButtons(
            down=win32con.WM_MBUTTONDOWN,
            up=win32con.WM_MBUTTONUP,
            key=win32con.MK_MBUTTON
        )
