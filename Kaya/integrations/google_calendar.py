import datetime
import os.path

from . import integration_base as ib
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from .models import audio_model as audio

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


class GoogleCalendar(ib.Integration):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    def __init__(self) -> None:
        """
        Init the integration
        """
        super().__init__()
        creds = None
        if os.path.exists("Kaya/secrets/token.json"):
            creds = Credentials.from_authorized_user_file(
                "Kaya/secrets/token.json", SCOPES
            )
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "Kaya/secrets/credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("Kaya/secrets/token.json", "w", encoding="utf8") as token:
                token.write(creds.to_json())
        self.service = build("calendar", "v3", credentials=creds)

    async def check(self, query: str) -> bool:
        """
        Check if the integration should be used
        """
        return any(
            match in query
            for match in (
                "what do i have today",
                "what do i have tomorrow",
                "what do i have on the",
                "what do i have on",
                "what's on my calendar",
                "what is on my calendar",
                "what's on my schedule",
                "what is on my schedule",
                "what's on my agenda",
                "what is on my agenda",
                "do i have anything today",
                "do i have anything tomorrow",
                "do i have anything on the",
                "do i have anything on",
                "do i have anything scheduled",
                "do i have anything scheduled today",
                "do i have anything scheduled tomorrow",
                "do i have anything scheduled on the",
                "do i have anything scheduled on",
                "do i have anything on my calendar",
                "do i have anything on my schedule",
            )
        )

    async def response(self, query: str, voice: audio.KayaAudio) -> str:
        """
        Response to the integration
        """

        now = datetime.datetime.utcnow().isoformat() + "Z"
        print("Getting the upcoming 10 events")
        events_result = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        for event in events:
            print(event)
            time = datetime.datetime.fromisoformat(event["start"]["dateTime"])
            await voice.say(
                f"you have {event['summary']} at {time.strftime('%I:%M %p')}"
            )
