"""
Kaya Main

This is just the program that runs Kaya and is not a part of Kaya herself.
"""

import audio
import brain


if __name__ == "__main__":
    audio = audio.KayaAudio()
    kaya = brain.KayaBrain(audio)
    while True:
        kaya.process_command()
