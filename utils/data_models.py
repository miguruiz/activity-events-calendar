from dataclasses import dataclass
import datetime as dt

@dataclass(frozen=False)  # Data class with mutable attributes
class Activity:
    """
    Represents an activity with various attributes.
    """
    unique_id:str  # Unique identifier for the activity
    name: str  # Name of the activity
    start_date: dt.date  # Start date of the activity
    end_date: dt.date  # End date of the activity
    club: str  # Club or organization hosting the activity
    kind_long: str  # Long description of the type of activity
    kind_sort:str  # Short description of the type of activity
    link: str  # Link to more information about the activity
    calendar_url: str  # URL of the calendar for the activity

@dataclass(frozen=True)  # Data class with immutable attributes
class Config:
    """
    Represents configuration settings for a system.
    """
    GOOGLE_CALENDAR_ID: str  # Google Calendar ID
    GOOGLE_SERVICE_ACCOUNT_FILE_PATH: str  # File path of the Google service account file
    TELEGRAM_CHAT_ID: str  # Chat ID for Telegram
    TELEGRAM_TOKEN: str  # Token for Telegram API
    ACTIVITY_VISITED_ACTIVITIES_PATH: str  # File path for storing visited activities
    IS_TEST: bool  # Boolean flag indicating if it's a test environment
