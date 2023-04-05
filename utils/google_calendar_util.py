from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import time

def create_calendar_event(activity, service, config):
    """
    Create a calendar event using the Google Calendar API.

    Args:
        activity (Activity): The activity object containing the details of the event.
        service (googleapiclient.discovery.Resource): The Calendar API service object.
        config (Config): The configuration object containing the necessary credentials and settings.

    Returns:
        tuple: A tuple containing a boolean value indicating whether the event creation was successful or not,
        and the URL of the created event if successful, or an error message if unsuccessful.
    """

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
        'visibility': 'default'
    }

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
    """
    Create calendar events for a list of activities using the Google Calendar API.

    Args:
        new_activities (dict): A dictionary containing Activity objects as values.
        config (Config): The configuration object containing the necessary credentials and settings.

    Returns:
        tuple: A tuple containing two lists - the list of activities for which events were successfully created,
        and the list of activities for which event creation failed.
    """

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
