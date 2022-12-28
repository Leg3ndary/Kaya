"""
Kaya Main

This is just the program that runs Kaya and is not a part of Kaya herself.
"""

import asyncio

from Kaya import audio, brain, gui

async def main() -> None:
    """
    The main function
    """
    loop = asyncio.get_event_loop()
    voice = audio.KayaAudio()
    kaya = brain.KayaBrain(voice)

    await kaya.welcome()
    kaya.gui = gui.KayaWindow()

    loop.run_in_executor(None, kaya.gui.run)

    while True:
        await kaya.process_command()

if __name__ == "__main__":
    asyncio.run(main())
