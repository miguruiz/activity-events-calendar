# Script
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

is_test = False


PRD_CALENDAR_ID = '05c835441608070151910c45bea2f990fdf70fb8c9a6a50adf01fc1b185a7e95@group.calendar.google.com'
TEST_CALENDAR_ID = '1c4487f9f1779a6ee2b67e4bff28c0a36e711a2ac6340cdc1ce9e3091942fe4c@group.calendar.google.com'
KEY_FILE_LOCATION = '/Users/miguruiz/Downloads/personal-mrn-d9d05a8cd966.json'

if is_test: 
    CALENDAR_ID = TEST_CALENDAR_ID
else:
    CALENDAR_ID = PRD_CALENDAR_ID

# Authenticate and create the service object.
creds = service_account.Credentials.from_service_account_file(KEY_FILE_LOCATION, scopes=['https://www.googleapis.com/auth/calendar'])
service = build('calendar', 'v3', credentials=creds)

try:
    # Call the API to list all events in the calendar.
    events_result = service.events().list(calendarId=CALENDAR_ID, maxResults=2500).execute()
    events = events_result.get('items', [])

    # Loop through all events and delete them.
    for event in events:
        print(f"Deleting: {event['summary']}")
        service.events().delete(calendarId=CALENDAR_ID, eventId=event['id']).execute()

except HttpError as error:
    print('An error occurred: %s' % error)
if not is_test: 
    print("end - Remember to delete activities.txt")
else:
    print("end")
