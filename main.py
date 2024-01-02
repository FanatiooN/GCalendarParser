import os
import pickle
import re

from pandas import Series
from Record import Record
from pandas import DataFrame
from datetime import datetime
from datetime import timedelta
from dotenv import load_dotenv
from SheetsParser import SheetsParser

from googleapiclient.discovery import build
from googleapiclient.discovery import Resource

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_current_month_events(service: Resource):
    now = datetime.now()
    start_date = datetime(now.year, now.month, 1).isoformat() + "Z"
    end_date = datetime(now.year, now.month + 1, 1).isoformat() + "Z"
    events = (
        service.events()
        .list(calendarId="primary", timeMin=start_date, timeMax=end_date)
        .execute()
    )
    return events["items"]


def extract_duration(s):
    match = re.search(r"\d+", s)
    if match:
        duration = int(match.group())
        if "час" in s:
            duration *= 60
        return duration
    else:
        return 0


def create_event(service: Resource, record: Series):
    fullname = record.fullname
    theme = record.theme
    date = record.date
    time = record.time
    duration = extract_duration(record.duration.value)

    dt = datetime.combine(date, time)
    date_start = dt.isoformat()
    date_end = (dt + timedelta(minutes=duration)).isoformat()

    event = {
        "summary": f"{fullname} | {theme}",
        "start": {
            "dateTime": date_start,
            "timeZone": "Europe/Moscow",
        },
        "end": {
            "dateTime": date_end,
            "timeZone": "Europe/Moscow",
        },
    }

    events = get_current_month_events(service=service)
    for e in events:
        if e["summary"] == event["summary"]:
            return

    event = service.events().insert(calendarId="primary", body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")


if __name__ == "__main__":
    with open("token.pickle", "rb") as token:
        creds = pickle.load(token)

    service = build("calendar", "v3", credentials=creds)

    load_dotenv()

    urls = [os.environ.get("table_url")]
    parser = SheetsParser(urls=urls)

    df = parser.parseSchedule()

    for index, row in df.iterrows():
        create_event(service=service, record=row)
