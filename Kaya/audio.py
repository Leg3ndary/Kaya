"""
Kaya's audio module, anything kaya says or listens too will first be processed here.
"""

import pyttsx3
import speech_recognition


class KayaAudio:
    """
    Kaya's audio module
    """

    def __init__(self) -> None:
        """
        Initialising Kaya's Audio Module
        """
        self.engine: pyttsx3.Engine = pyttsx3.init()
        self.engine.setProperty("voice", self.engine.getProperty("voices")[1].id)
        self.set_rate(150)

    def set_rate(self, rate: int) -> None:
        """
        Set the rate at which Kaya speaks
        """
        self.voicespeed = rate
        self.engine.setProperty("rate", self.voicespeed)

    async def say(self, audio: str) -> None:
        """
        Say something out loud
        """
        self.engine.say(audio)
        self.engine.runAndWait()
        return

    async def take_command(self) -> str:
        """
        Takes a command for processing
        """
        recog = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as source:
            print("Listening...")
            recog.pause_threshold = 1
            audio = recog.listen(source)

        try:
            print("Recognising...")
            query = recog.recognize_google(audio, language="en-us")
        except Exception as exc:
            print(exc)
            return "---"
        return query
