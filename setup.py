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
]
options = {
    "build_exe": {
        "packages": packages,
    },
}

setup(
    name="Kaya",
    options=options,
    version="0.1.0",
    description="Kaya PA",
    executables=executables,
)
