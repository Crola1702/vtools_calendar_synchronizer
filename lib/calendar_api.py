import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .entity.event import Event

class CalendarAPI:
    SCOPES = [
        "https://www.googleapis.com/auth/calendar.events",
        "https://www.googleapis.com/auth/calendar.calendarlist",
    ]

    def __init__(self, calendar_id):
        self.creds = None
        self.calendar_id = calendar_id

        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if os.path.exists("credentials.json"):
                    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.SCOPES)
                    self.creds = flow.run_local_server(port=0)
                else:
                    raise FileNotFoundError()

            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

        try:
            self.service = build("calendar", "v3", credentials=self.creds)
        except HttpError as error:
            print(f"An error occurred: {error}")

    def get_all_events(self):
        try:
            return self.service.events().list(calendarId=self.calendar_id).execute()['items']
        except HttpError as error:
            print(f"An error occurred: {error}")
            raise error

    def get_event(self, event_id: str):
        try:
            return self.service.events().get(calendarId=self.calendar_id, eventId=event_id).execute()
        except HttpError as error:
            if error.status_code == 404:
                return None
            print(f"An error occurred: {error}")

    def add_or_update_event(self, event: Event):
        try:
            existing_event = self.get_event(event.id)
            if existing_event:
                cal_event = Event.from_calendar_event(existing_event)
                if cal_event != event or cal_event.cal_status == 'cancelled':
                    self.update_event(event)
                    return 'updated'
                else:
                    return 'no_change'
            else:
                self.add_event(event)
                return 'added'
        except HttpError as error:
            print(f"An error occurred: {error}")
            raise error
            


    def add_event(self, event: Event):
        try:
            self.service.events().insert(calendarId=self.calendar_id, body=event.to_calendar_event()).execute()
        except HttpError as error:
            print(f"An error occurred: {error}")
            raise error

    def update_event(self, event: Event):
        try:
            self.service.events().patch(calendarId=self.calendar_id, eventId=event.id, body=event.to_calendar_event()).execute()
        except HttpError as error:
            print(f"An error occurred {error}")
            raise error

    def delete_event(self, event_id: str):
        try:
            self.service.events().delete(calendarId=self.calendar_id, eventId=event_id).execute()
        except HttpError as error:
            print(f"An error occurred: {error}")
            raise error

    def clear_all_events(self):
        events = self.get_all_events()
        for event in events:
            self.delete_event(event['id']) 
