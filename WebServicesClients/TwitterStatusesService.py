from WebServicesClients.WebServiceBase import WebServiceBase


class TwitterStatusesService(WebServiceBase):

    HOME_TIMELINE_URL = "/1.1/statuses/home_timeline.json"
    UPDATE_URL = "/1.1/statuses/update.json"

    def __init__(self, base_url, consumer_key, consumer_secret, access_token, access_token_secret):
        super().__init__(base_url, consumer_key, consumer_secret, access_token, access_token_secret)

    def get_home_timeline(self):
        return self._get(self.HOME_TIMELINE_URL)

    def post_tweet(self, payload):
        return self._post(self.UPDATE_URL, payload)
