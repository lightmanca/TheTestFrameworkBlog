from WebServicesClients.WebServiceBase import WebServiceBase


class TwitterStatusesService(WebServiceBase):

    # All URLS variable names need to end in '_URL".  We do some python magic to add the base url to the front of the
    # variables.
    HOME_TIMELINE_URL = "/1.1/statuses/home_timeline.json"
    UPDATE_URL = "/1.1/statuses/update.json"
    DESTROY_STATUS_URL = "/1.1/statuses/destroy/{status_id}.json"

    def __init__(self, base_url, oauth_creds, logger_id):
        super().__init__(base_url, oauth_creds, logger_id)

    def get_home_timeline(self):
        return self._get(self.HOME_TIMELINE_URL)

    def post_tweet(self, payload):
        return self._post(self.UPDATE_URL, payload)

    def delete_status(self, status_id):
        url = self.DESTROY_STATUS_URL.format(status_id=status_id)
        return self._post(url, None)
