from win32 import win32clipboard

class Clipboard:
    @staticmethod
    def get_clipboard() -> str:
        win32clipboard.OpenClipboard()
        try: result = win32clipboard.GetClipboardData()
        except TypeError: result = None
        win32clipboard.CloseClipboard()
        return result

    @staticmethod
    def set_clipboard(content: str) -> None:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(content, win32clipboard.CF_TEXT)
        win32clipboard.CloseClipboard()
