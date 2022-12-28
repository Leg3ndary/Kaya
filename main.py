"""
Kaya Main

This is just the program that runs Kaya and is not a part of Kaya herself.
"""

import asyncio

import threading
from Kaya import audio, brain, gui

class Kaya(threading.Thread):
    """
    Kaya
    """

    def __init__(self, tk_root) -> None:
        """
        Init Kaya
        """
        self.root = tk_root

        self.loop = asyncio.get_event_loop()

        threading.Thread.__init__(self)
        self.start()

    def run(self) -> None:
        """
        Run Kaya
        """
        self.loop.run_until_complete(start())

async def start() -> None:
    """
    Start Kaya
    """
    voice = audio.KayaAudio()
    kaya = brain.KayaBrain(voice)

    await kaya.welcome()

    while True:
        await kaya.process_command()

def main() -> None:
    """
    The main function
    """
    win = gui.KayaWindow()
    Kaya(win)
    win.load()


if __name__ == "__main__":
    main()
