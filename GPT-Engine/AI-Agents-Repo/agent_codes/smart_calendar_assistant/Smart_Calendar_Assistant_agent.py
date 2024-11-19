
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_account():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('calendar', 'v3', credentials=creds)

def create_event(service, start_time_str, end_time_str, summary, description=None, location=None):
    start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
    event_result = service.events().insert(calendarId='primary',
        body={
            "summary": summary,
            "description": description,
            "location": location,
            "start": {"dateTime": start_time.strftime("%Y-%m-%dT%H:%M:%S"), "timeZone": 'Asia/Kolkata'},
            "end": {"dateTime": end_time.strftime("%Y-%m-%dT%H:%M:%S"), "timeZone": 'Asia/Kolkata'},
        }
    ).execute()
    return event_result['id']

def delete_event(service, event_id):
    try:
        service.events().delete(
            calendarId='primary',
            eventId=event_id,
        ).execute()
    except googleapiclient.errors.HttpError:
        print("Failed to delete event")

class SmartCalendarAssistant:
    def __init__(self):
        self.service = authenticate_google_account()

    def add_event(self, start_time_str, end_time_str, summary, description=None, location=None):
        return create_event(self.service, start_time_str, end_time_str, summary, description, location)

    def remove_event(self, event_id):
        delete_event(self.service, event_id)

if __name__ == '__main__':
    assistant = SmartCalendarAssistant()
    event_id = assistant.add_event('2023-09-30 10:00:00', '2023-09-30 12:00:00', 'Meeting with team', 'Planning for next project')
    print("Event created: ", event_id)
    assistant.remove_event(event_id)
    print("Event deleted")
