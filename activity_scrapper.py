import os
import warnings
import datetime as dt
import time
import random
from utils import telegram_util as telegram
from activity_sources import cam
from utils import google_calendar_util as google
from utils.utils import get_configuration
from utils import aws_s3 as aws

warnings.filterwarnings("ignore")

def concat_activities(*dicts):
    result_dict = {}
    try:    
        for dct in dicts:
            result_dict.update(dct)
    except Exception as error:
        print(f"An error occurred creating the dict: {error}")
        #TODO: Send notification to Telegram! Saying that the execution failed in the dict!
    return result_dict

    result_dict = {}
    for dct in dicts:
        result_dict.update(dct)
    return result_dict

def read_visited_activity_ids(config):
    f = ''
    if not config.IS_TEST:
        if 's3' in config.ACTIVITY_VISITED_ACTIVITIES_PATH:
            f = aws.read_from_s3(config.ACTIVITY_VISITED_ACTIVITIES_PATH)
        else:
             if os.path.isfile(os.path.expanduser(config.ACTIVITY_VISITED_ACTIVITIES_PATH)):
                print(f"{config.ACTIVITY_VISITED_ACTIVITIES_PATH} was found loading!")
                with open(os.path.expanduser(config.ACTIVITY_VISITED_ACTIVITIES_PATH), 'r') as file:
                    f = file.read()  # Read contents and remove leading/trailing whitespaces
    return set(f.strip().split(','))

def get_new_activities(activities, visited_activities):
    new_activities_id = set(activities.keys()).difference(visited_activities)
    return {k: v for k, v in activities.items() if k in new_activities_id}


def persist_results(success, visited, config):
    all = set(success).union(visited)
    to_persist = ",".join([a.unique_id for a in all]) + ","
    if not config.IS_TEST:
        if 's3' in config.ACTIVITY_VISITED_ACTIVITIES_PATH:
            aws.write_to_s3(config.ACTIVITY_VISITED_ACTIVITIES_PATH, to_persist)
        else:
            with open(os.path.expanduser(config.ACTIVITY_VISITED_ACTIVITIES_PATH), "a+") as f:
                f.write(to_persist)
        
def generate_final_report(new_activities, success, failed,visited_activities, config):
    cur_exec = dt.datetime.now()

    final_report = f"""
    {cur_exec.day}.{cur_exec.month}.{cur_exec.year} {cur_exec.hour}:{cur_exec.minute} CET
    === SUMMARY === {"test" if config.IS_TEST else ""}
    
    - NEW:       {len(new_activities)} new activities found!
    - SUCCESSFUL: {len(success)} calendar events created.
    - FAILED:    {len(failed)} calendar events that failed to be created.
    """
    telegram.send_telegram_msg(final_report, config)
    
    if config.IS_TEST:
        new_activities = random.sample(list(new_activities), 3)

    for a in new_activities:
        to_send = f"""NEW ACTIVITY - {a.club} - {"test" if config.IS_TEST else ""}

{a.kind_long} - {a.name}

Dates {a.start_date} to {a.end_date}

Activity Link: {a.link}
"""
        telegram.send_telegram_msg(to_send, config)
        time.sleep(0.2)
    return final_report
    
def main():
    is_test = False

    config = get_configuration('/tmp/config.ini', is_test)

    # Get Sources
    cam_activities = cam.get_activities_from_cam()

    # Concatenate all activities and compute new ones
    all_activities = concat_activities(cam_activities)
    visited_activities = read_visited_activity_ids(config)
    new_activities = get_new_activities(all_activities,visited_activities)

    # Create calendar events
    success, failed = google.create_calendar_events(new_activities, config)

    if success: 
        persist_results(success,visited_activities, config)

    r= generate_final_report(new_activities.values(),success, failed, config)
    print(r)

if __name__ == "__main__":
    main()
