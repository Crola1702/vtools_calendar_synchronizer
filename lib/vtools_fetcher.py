import requests
from .entity.event import Event

class EventFetcher:

    base_url = ''
    event_limit = 2000

    def __init__(self, base_url = "https://events.vtools.ieee.org/RST/events/api/public/v5/", event_limit = 1000):
        self.base_url = base_url
        self.event_limit = event_limit

    def filter_event_by_country(self,event, country_id):
        country_data = event['relationships']['country'].get('data')
        if not country_data:
            return False

        return int(country_data['id']) == country_id

    def fetch_countries(self):
        return requests.get(self.base_url + f"countries/list").json()['data']

    def fetch_events(self):
        return requests.get(self.base_url + f"events/list?span=now~&limit={self.event_limit}&sort=+start_time").json()['data']

    def get_events_by_country(self,country_id):
        return list(map(lambda x: Event(**x['attributes']), filter(lambda x: self.filter_event_by_country(x, country_id), self.fetch_events())))
