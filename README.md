# activity-events-calendar


TODO: add subscription date to CAM!
TODO: add other sources
TODO: is_test should come as a param as a param
TODO: create dry_run param

TODO: CICD -> create the zip, upload it to s3



How it works?
Extracts activities, checks against visited, if new, adds a calendar event.

- Create service account in google
- Create a calendar and share it with the service account google-calendar-bot@personal-mrn.iam.gserviceaccount.com

- Telegram bot + token
- Aws for credentials, activities.txt & credentials for google

- test ignores visited_activities, and adds events to a test calendar.