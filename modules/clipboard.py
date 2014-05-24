import win32clipboard, win32con

class Clipboard(object):
    def __enter__(self):
        win32clipboard.OpenClipboard()
        return self

    def __exit__(self, *exit_info):
        win32clipboard.CloseClipboard()

    def get(self, format):
        if win32clipboard.IsClipboardFormatAvailable(format):
            return win32clipboard.GetClipboardData(format)
        else:
            return None

    def set(self, format, data):
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(format, data)

clipboard = Clipboard()

def get_files():
    with clipboard as c:
        return c.get(win32con.CF_HDROP)

def get_text():
    with clipboard as c:
        return c.get(win32con.CF_TEXT)

def get_bmp():
    if win32clipboard.IsClipboardFormatAvailable(win32con.CF_DIB):
        from PIL import ImageGrab
        image = ImageGrab.grabclipboard()
        return image
    else:
        return None

def set_text(value):
    with clipboard as c:
        c.set(win32con.CF_UNICODETEXT, value)
