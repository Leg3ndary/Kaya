"""
Integration Base Class
"""

from .models import audio_model as audio


class Integration:
    """
    Base class for integration
    """

    def __init__(self) -> None:
        """
        Init the integration
        """
        self.multi = False

    async def check(self, query: str) -> bool:
        """
        Check if the integration should handle the query, must return a bool
        """
        return False

    async def response(self, query: str, voice: audio.KayaAudio) -> None:
        """
        The code that should be ran if the check is correct
        """
