from dataclasses import dataclass
import datetime as dt

@dataclass(frozen=False)
class Activity:
    unique_id:str
    name: str
    start_date: dt.date
    end_date: dt.date
    club: str
    kind_long: str
    kind_sort:str
    link: str
    calendar_url: str

@dataclass(frozen=True)
class Config:
    GOOGLE_CALENDAR_ID: str
    GOOGLE_SERVICE_ACCOUNT_FILE_PATH: str
    TELEGRAM_CHAT_ID: str
    TELEGRAM_TOKEN: str
    ACTIVITY_VISITED_ACTIVITIES_PATH: str
    IS_TEST: bool
