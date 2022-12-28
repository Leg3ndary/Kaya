"""
Kaya's brain, this is where almost all of the stuff is done
"""

import datetime
import json
from typing import Optional

import audio
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

    def get_time(self) -> None:
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
        self.voice.say(f"It is {time_str}")

    def get_date(self) -> None:
        """
        Get the date
        """
        date_str = datetime.datetime.now().strftime("%A, %B, %dth, %Y")
        self.voice.say(f"It is {date_str}")

    def process_command(self) -> Optional[str]:
        """
        process a command
        """
        query = self.voice.take_command().lower()
        print(query)

        if query == "---":
            return

        if any(
            match in query.replace(" current ", " ")
            for match in ("what's the time", "what time is it", "what is the time")
        ):
            self.get_time()

        elif any(
            match in query
            for match in (
                "what day is it",
                "what's the date",
                "what is the date",
                "what date is it",
            )
        ):
            self.get_date()

        else:
            API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"
            headers = {"Authorization": f"Bearer {self.config.get('huggingface')}"}

            payload = {
                "inputs": query,
            }

            response = httpx.post(API_URL, headers=headers, json=payload)
            print(response.json())
            self.voice.say(response.json().get("generated_text"))
