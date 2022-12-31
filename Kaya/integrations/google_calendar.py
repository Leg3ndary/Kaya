import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

class GoogleCalendarIntegration:
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    def __init__(self) -> None:
        """
        Init the integration
        """
        creds = None
        if os.path.exists("Kaya/secrets/token.json"):
            creds = Credentials.from_authorized_user_file("Kaya/secrets/token.json", SCOPES)
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

        try:
            service = build("calendar", "v3", credentials=creds)

            now = datetime.datetime.utcnow().isoformat() + "Z"
            print("Getting the upcoming 10 events")
            events_result = (
                service.events()
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
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(start, event["summary"])

        except HttpError as error:
            print(f"An error occurred: {error}")
