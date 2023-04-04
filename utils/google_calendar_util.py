from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import time

def create_calendar_event(activity, service, config):
    # doc: https://developers.google.com/calendar/api/v3/reference/events#resource

    event = {
        'summary': f'{activity.unique_id[:2]}]{activity.kind_sort}-{activity.name} - {activity.club}',
        'description': f""" {activity.kind_long}- {activity.club} - {activity.link}""",
        'start': {
            'date': activity.start_date.strftime('%Y-%m-%d'),
            'timeZone': 'Europe/Madrid',
        },
        'end': {
            'date': activity.end_date.strftime('%Y-%m-%d'),
            'timeZone': 'Europe/Madrid',
        },
        'transparency': 'transparent',
        'visibility': 'default'}
    try:
        print(f"Creating: /n {event}")
        event = service.events().insert(calendarId=config.GOOGLE_CALENDAR_ID, body=event).execute()
        print(f"Event created: {activity.unique_id} - {activity.name} - {event.get('htmlLink')}")
        result = (True, event.get('htmlLink'))

    except Exception as error:
        print(f"An error occurred: {error}")
        result = (False, "err")

    return result


def create_calendar_events(new_activities, config):
    # create credentials object from service account JSON key file
    creds = Credentials.from_service_account_file(config.GOOGLE_SERVICE_ACCOUNT_FILE_PATH,
                                                  scopes=['https://www.googleapis.com/auth/calendar'])
    # build the API client
    service = build('calendar', 'v3', credentials=creds)
    success = []
    failed = []

    for activity in new_activities.values():
        result = create_calendar_event(activity, service, config)
        if result[0]:
            activity.calendar_url = result[1]
            success.append(activity)
        else:
            activity.calendar_url = result[1]
            failed.append(activity)
        time.sleep(0.2)

    return success, failed