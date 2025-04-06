import requests
from .entity.event import Event

class EventFetcher:
    BASE_URL = 'https://events.vtools.ieee.org/RST/events/api/public/v5/'
    EVENT_LIMIT = 1000

    def __init__(self, base_url='', event_limit=None):
        self.base_url = base_url if base_url else self.BASE_URL
        self.event_limit = event_limit if event_limit else self.EVENT_LIMIT

    def filter_event_by_country(self, event, country_id):
        country_data = event['relationships']['country'].get('data')
        if not country_data:
            return False
        
        return str(country_data['id']) == str(country_id)

    def fetch_events(self):
        return requests.get(self.base_url + f"events/list?limit={self.event_limit}").json()['data']

    def get_events_by_country(self, country_id):
        return list(map(lambda x: Event(**x['attributes']), filter(lambda x: self.filter_event_by_country(x, country_id), self.fetch_events())))
