from utils.utils import generate_id
from bs4 import BeautifulSoup
import requests
from utils.data_models import Activity
import utils.utils as utils
import datetime as dt
def get_activities_from_cam():
    # TODO: GET THE DATE TO JOIN!!

    # Send a GET request to the first page of the website
    url = 'https://clubalpino.es/actividades'

    response = requests.get(url)

    # Use Beautiful Soup to parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the activity elements on the page
    pages = soup.find_all('a', {'class': 'page-numbers'})
    pages_to_visit = [p['href'] for p in pages]

    activities = {}

    for url in pages_to_visit:
        response = requests.get(url)

        # Use Beautiful Soup to parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the activity elements on the page
        activity_elements = soup.find_all('td', {'class': 'list_text'})

        # Loop through each activity element and extract the relevant information
        for activity_element in activity_elements:
            activity_name = activity_element.h3.text
            activity_date = activity_element.find('span', {'class': 'ribbon'}).text.strip()
            start_date = activity_date.split(' – ')[0]
            end_date = activity_date.split(' – ')[1]
            activity_kind = activity_element.find('p', {'class': 'event_meta'}).text.split('\xa0')[-1]
            activity_link = activity_element.find('a', href=True)['href']
            unique_id = generate_id(start_date + activity_link)

            if activity_kind in utils.activity_filter_out:
                continue
            parsed_activity = Activity(
                unique_id=unique_id,
                name=activity_name,
                start_date=dt.datetime.strptime(start_date, '%d/%m/%Y').date(),
                end_date=dt.datetime.strptime(end_date,
                                              '%d/%m/%Y').date() if end_date == start_date else dt.datetime.strptime(
                    end_date, '%d/%m/%Y').date() + dt.timedelta(days=1),
                club='CAM',
                kind_long=activity_kind,
                kind_sort=utils.activity_kind_mapper[activity_kind] if activity_kind in utils.activity_kind_mapper else activity_kind,
                link=activity_link,
                calendar_url=None
            )

            activities[unique_id] = parsed_activity
    return activities