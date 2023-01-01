"""
Kaya's brain, this is where almost all of the stuff is done
"""

import datetime
import json
import random
from typing import Optional, List

import httpx

from . import audio, gui
from .integrations import integration_base as ib
from .integrations import time_re


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
        self.integrations: List[ib.Integration] = [
            time_re.TimeRe(),
            time_re.DateRe()
        ]

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
        Process a command/integration
        """
        query = (await self.voice.take_command()).lower()
        print(query)

        answered = False

        for integration in self.integrations:
            if await integration.check(query):
                if not integration.multi and answered:
                    continue
                answered = True
                return await integration.response(self.voice)
        
        if not answered:
            API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"
            headers = {"Authorization": f"Bearer {self.config.get('huggingface')}"}

            payload = {
                "inputs": query,
            }

            response = httpx.post(API_URL, headers=headers, json=payload)
            print(response.json())
            await self.voice.say(response.json()[0].get("generated_text"))