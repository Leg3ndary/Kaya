import datetime

from . import integration_base as ib
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
        self.multi = False

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


class DateRe(ib.Integration):
    """
    Date integration
    """

    def __init__(self) -> None:
        """
        Init the date integration
        """
        super().__init__()
        self.multi = False

    async def check(self, query: str) -> bool:
        """
        Check if the query is a date query
        """
        return any(
            match in query
            for match in (
                "what day is it",
                "what's the date",
                "what is the date",
                "what date is it",
            )
        )

    async def response(self, voice: audio.KayaAudio) -> str:
        """
        Get the date
        """
        date_str = datetime.datetime.now().strftime("%A, %B, %dth, %Y")
        await voice.say(f"it is {date_str}")
