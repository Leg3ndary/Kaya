from . import integration_base as ib
import datetime

from .models import audio_model as audio

class TimeRe(ib.Integration):
    """
    Time integration
    """

    def __init__(self) -> None:
        """
        Init the time integration
        """
        super().__init__()
        self.multi = True

    async def check(self, query: str) -> bool:
        """
        Check if the query is a time query
        """
        return any(
            match in query.replace(" current ", " ")
            for match in ("what's the time", "what time is it", "what is the time")
        )

    async def response(self, voice: audio.KayaAudio) -> str:
        """
        Get the time
        """
        now = datetime.datetime.now()

        hour = str(now.hour if now.hour < 13 else now.hour - 12)
        minute = str(now.strftime("%H"))
        if minute[0] == "0":
            minute = "o" + minute[1]
        meridiem = datetime.datetime.now().strftime("%p").lower()
        time_str = f"{hour} {minute} {meridiem}"
        await voice.say(f"it is {time_str}")
