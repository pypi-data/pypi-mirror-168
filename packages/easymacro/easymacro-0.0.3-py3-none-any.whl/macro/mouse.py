from .window import Window
from .utils import ScreenCoordinates, MouseButtons
from win32 import win32gui, win32api

class Mouse:
    def __init__(self, *, window: Window = None) -> None:
        self.window = window
        self.clipped = False
    
    def get_position(self) -> ScreenCoordinates:
        x, y = win32gui.GetCursorPos()
        return ScreenCoordinates(x, y)
    
    def set_position(self, coordinates: ScreenCoordinates) -> None:
        x, y = coordinates.__tuple__()
        win32api.SetCursorPos((x, y))

    def clip(self, *, coordinates: ScreenCoordinates, coordinates2: ScreenCoordinates = None, set_position: bool = False) -> None:
        if coordinates2 is None:
            coordinates2 = coordinates
        x, y = coordinates.__tuple__()
        x2, y2 = coordinates2.__tuple__()
        win32api.ClipCursor((x - 1, y - 1, x2 + 1, y2 + 1))
        if set_position:
            self.set_position(ScreenCoordinates((x + x2) / 2, (y + y2) / 2))
        self.clipped = True
    
    def unclip(self) -> None:
        if not self.clipped:
            return
        win32api.ClipCursor((0, 0, 0, 0))
        self.clipped = False

    def click_down(self, *, window: Window = None, coordinates: ScreenCoordinates = None, button: MouseButtons) -> None:
        if coordinates is None:
            coordinates = self.get_position()
        if window is None:
            if self.window is not None:
                window = self.window
            else:
                window = Window.get_current()

        longcoords = win32api.MAKELONG(coordinates.x, coordinates.y)
        win32gui.SendMessage(window.get_hwnd(), button.down, button.key, longcoords)
    
    def click_up(self, *, window: Window = None, coordinates: ScreenCoordinates = None, button: MouseButtons) -> None:
        if coordinates is None:
            coordinates = self.get_position()
        if window is None:
            if self.window is not None:
                window = self.window
            else:
                window = Window.get_current()

        longcoords = win32api.MAKELONG(coordinates.x, coordinates.y)
        win32gui.SendMessage(window.get_hwnd(), button.up, None, longcoords)
    
    def click(self, *, window: Window = None, coordinates: ScreenCoordinates = None, button: MouseButtons) -> None:
        self.click_down(window=window, coordinates=coordinates, button=button)
        self.click_up(coordinates=coordinates, button=button)
