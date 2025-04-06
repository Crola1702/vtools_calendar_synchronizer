import os
import argparse
from lib.vtools_fetcher import EventFetcher
from lib.calendar_api import CalendarAPI
from dotenv import load_dotenv

parser = argparse.ArgumentParser(description="Fetch events from vTools and add them to Google Calendar")
parser.add_argument('--vtools-api', type=str, help='vTools API URL')
parser.add_argument('--event-limit', type=int, help='Limit of events to fetch from vTools')
parser.add_argument('-c', '--calendar-id', type=str, help='Google Calendar ID')
parser.add_argument('-co', '--country-id', type=str, help='Country ID to filter events')
args = parser.parse_args()

load_dotenv()

vtools_api = os.getenv('VTOOLS_API') or args.vtools_api
event_limit = os.getenv('EVENT_LIMIT') or args.event_limit
calendar_id = os.getenv('CALENDAR_ID') or args.calendar_id
country_id = os.getenv('COUNTRY_ID') or args.country_id

if calendar_id is None:
    raise ValueError("CALENDAR_ID is not set")
if country_id is None:
    raise ValueError("COUNTRY_ID is not set")


vtf = EventFetcher(base_url=vtools_api, event_limit=event_limit)

print("Fetching events from vTools")
events = vtf.get_events_by_country(country_id)
print(f"{len(events)} Events fetched")

print("Bootstraping CalendarAPI")
calendar = CalendarAPI(calendar_id)
print("Bootstraped CalendarAPI")

stats = {'added': 0, 'updated': 0, 'no_change': 0}
print("Adding/Updating events to Google Calendar")
for event in events:
    result = calendar.add_or_update_event(event)
    stats[result] += 1

print(f"Added: {stats['added']}")
print(f"Updated: {stats['updated']}")
print(f"No Change: {stats['no_change']}")
print("Done")
