from .utils import ScreenCoordinates
from win32 import win32gui, win32process
from win32.lib import win32con

class Window:
    def __init__(self, hwnd) -> None:
        self.hwnd = hwnd
        if self.hwnd == 0: self.hwnd = None

    def __eq__(self, __o: object) -> bool:
        return self.get_hwnd() == __o.get_hwnd()

    @staticmethod
    def get_current():
        return Window(win32gui.GetForegroundWindow())

    @staticmethod
    def find_by_title(title: str):
        windows = []
        def callback(hwnd: int, _):
            window = Window(hwnd)
            if title.lower() in window.get_title().lower():
                windows.append(window)
        win32gui.EnumWindows(callback, None)
        return windows

    @staticmethod
    def find_by_class(clazz: str):
        windows = []
        def callback(hwnd: int, _):
            window = Window(hwnd)
            if clazz.lower() in window.get_class().lower():
                windows.append(window)
        win32gui.EnumWindows(callback, None)
        return Window(win32gui.FindWindow(clazz, None))

    @staticmethod
    def exists_by_title(title: str):
        return Window.find_by_title(title).get_hwnd() is not None

    @staticmethod
    def exists_by_class(clazz: str):
        return Window.find_by_class(clazz).get_hwnd() is not None

    def exists(self) -> bool:
        return self.get_hwnd() is not None

    def get_hwnd(self) -> int:
        return self.hwnd

    def get_pid(self) -> int:
        result = win32process.GetWindowThreadProcessId(self.get_hwnd())
        if len(result) > 0: return result[1]
        else: return None

    def get_class(self) -> str:
        return win32gui.GetClassName(self.get_hwnd())

    def get_title(self) -> str:
        return win32gui.GetWindowText(self.get_hwnd())

    def set_title(self, title: str) -> None:
        win32gui.SetWindowText(self.get_hwnd(), title)

    def set_position(self, *, coordinates: ScreenCoordinates, center: bool = True) -> None:
        x, y = coordinates.__tuple__()
        win_x, win_y, girth, length = win32gui.GetWindowRect(self.get_hwnd())
        width = girth - win_x
        height = length - win_y
        if center:
            x, y = ScreenCoordinates(x - (width / 2), y - (height / 2)).__tuple__()
        win32gui.SetWindowPos(self.get_hwnd(), win32con.HWND_NOTOPMOST, x, y, width, height, win32con.SWP_ASYNCWINDOWPOS)

    def is_active(self) -> bool:
        return Window.get_current().get_hwnd() == self.get_hwnd()

    def activate(self) -> None:
        win32gui.ShowWindow(self.get_hwnd(), win32con.SW_SHOW)

    def close(self) -> None:
        win32gui.PostMessage(self.get_hwnd(), win32con.WM_CLOSE, 0, 0)

    def maximise(self, *, activate: bool = True) -> None:
        win32gui.ShowWindow(self.get_hwnd(), win32con.SW_MAXIMIZE)
        if activate:
            self.activate()

    def minimise(self) -> None:
        win32gui.ShowWindow(self.get_hwnd(), win32con.SW_MINIMIZE)
