import sys

from cx_Freeze import Executable, setup

sys.setrecursionlimit(1500)

base = None  # "Win32GUI"

executables = [Executable("main.py", base=base)]

packages = [
    "speech_recognition",
    "pyttsx3",
    "httpx",
    "datetime",
    "json",
    "typing",
    "os",
    "sys",
    "threading",
    "asyncio",
    "tkinter",
    "PIL",
    "itertools",
    "pywintypes",
    "win32api",
    "win32con",
    "random",
]
options = {
    "build_exe": {
        "packages": packages,
    },
}

setup(
    name="Kaya",
    options=options,
    version="0.1.1",
    description="Kaya Personal Assistant.",
    executables=executables,
)
