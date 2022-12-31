"""
Audio model for type checking
"""

import pyttsx3

class KayaAudio:
    """
    Kaya's audio module
    """

    def __init__(self) -> None:
        """
        Initialising Kaya's Audio Module
        """
        self.engine: pyttsx3.Engine

    def set_rate(self, rate: int) -> None:
        """
        Set the rate at which Kaya speaks
        """

    async def say(self, audio: str) -> None:
        """
        Say something out loud
        """

    async def take_command(self) -> str:
        """
        Takes a command for processing
        """
