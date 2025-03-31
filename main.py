import os
from lib.vtools_fetcher import EventFetcher
from lib.calendar_api import CalendarAPI
from dotenv import load_dotenv

load_dotenv()

vtf = EventFetcher(base_url=os.getenv('VTOOLS_API'))

country_code = os.getenv('COUNTRY_CODE')

# TODO: Create exception class for this error
if country_code is None:
    raise Exception()

country_code = country_code.upper()
country_id = None
countries = vtf.fetch_countries()
for country in countries:
    id = country['id']
    abbreviation = country['attributes']['abbreviation']
    if abbreviation == country_code:
        country_id = id
        break

# TODO: Create exception class for this error
if country_id is None:
    raise Exception()

print("Fetching events from vTools")
events = vtf.get_events_by_country(int(country_id))
print(f"{len(events)} Events fetched")

print("Bootstraping CalendarAPI")
calendar = CalendarAPI(os.getenv("CALENDAR_ID"))
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
