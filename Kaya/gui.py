import tkinter
from itertools import count, cycle

import pywintypes
import win32api
import win32con
from PIL import Image, ImageTk


class ImageLabel(tkinter.Label):
    """
    A Label that displays images, and plays them if they are gifs
    """

    delay: int
    frames: list

    def load(self, im: str) -> None:
        """
        Load the label
        """
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info["duration"]
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self) -> None:
        """
        Unload the label
        """
        self.config(image=None)
        self.frames = None

    def next_frame(self) -> None:
        """
        Next frame
        """
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)


class KayaWindow:
    """
    Kaya's custom window
    """

    def __init__(self) -> None:
        """
        Init the window
        """
        self.win = tkinter.Tk()

        self.win.geometry("280x280")

        self.label = ImageLabel(self.win)

        self.win.overrideredirect(True)
        self.win.geometry("-0-0")
        self.win.lift()
        self.win.wm_attributes("-topmost", True)
        self.win.wm_attributes("-disabled", True)
        self.win.wm_attributes("-transparentcolor", "white")
        self.win.wm_attributes("-alpha", 0.2)

        hWindow = pywintypes.HANDLE(int(self.win.frame(), 16))
        exStyle = (
            win32con.WS_EX_COMPOSITED
            | win32con.WS_EX_LAYERED
            | win32con.WS_EX_NOACTIVATE
            | win32con.WS_EX_TOPMOST
            | win32con.WS_EX_TRANSPARENT
        )
        win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

    def load(self) -> None:
        """
        Load the window
        """
        print("Loading window...")
        self.label.pack()
        self.label.load("Kaya/icons/icon.gif")

        self.win.mainloop()
