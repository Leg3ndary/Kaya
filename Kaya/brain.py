"""
Kaya's brain, this is where almost all of the stuff is done
"""

import datetime
import json
import random
from typing import Optional

from . import audio, gui
import httpx


class KayaBrain:
    """
    Kaya's brain, all commands are processed here to actually do things
    """

    def __init__(self, voice: audio.KayaAudio) -> None:
        """
        Initialising Kaya's Brain
        """
        self.voice = voice
        with open("config.json", "r", encoding="utf8") as file:
            self.config = json.loads(file.read())
        self.gui: gui.KayaWindow

    async def get_time(self) -> None:
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
        await self.voice.say(f"It is {time_str}")

    async def get_date(self) -> None:
        """
        Get the date
        """
        date_str = datetime.datetime.now().strftime("%A, %B, %dth, %Y")
        await self.voice.say(f"It is {date_str}")

    async def welcome(self) -> None:
        """
        Welcome us back
        """
        now = datetime.datetime.now()
        time_of_day = (
            "morning" if now.hour < 12 else "afternoon" if now.hour < 17 else "evening"
        )
        greetings = (
            f"good {time_of_day} sir",
            "welcome back sir",
            "how can i help you sir",
            "what can i do for you sir",
            "how can i be of service sir",
        )
        await self.voice.say(random.choice(greetings))

    async def process_command(self) -> Optional[str]:
        """
        process a command
        """
        query = (await self.voice.take_command()).lower()
        print(query)

        if query == "---":
            return

        if any(
            match in query.replace(" current ", " ")
            for match in ("what's the time", "what time is it", "what is the time")
        ):
            await self.get_time()

        elif any(
            match in query
            for match in (
                "what day is it",
                "what's the date",
                "what is the date",
                "what date is it",
            )
        ):
            await self.get_date()

        else:
            API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"
            headers = {"Authorization": f"Bearer {self.config.get('huggingface')}"}

            payload = {
                "inputs": query,
            }

            response = httpx.post(API_URL, headers=headers, json=payload)
            print(response.json())
            await self.voice.say(response.json()[0].get("generated_text"))
