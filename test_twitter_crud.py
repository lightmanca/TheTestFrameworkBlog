import random
import string
import urllib
from urllib.parse import urlencode

import oauth2


class TestTwitterCRUD:

    CONSUMER_KEY = "<your consumer key>"
    CONSUMER_SECRET = "<your consumer secret>"
    ACCESS_TOKEN = "<your access token>"
    ACCESS_TOKEN_SECRET = "<your access token secret>"

    def test_get_timeline(self):
        home_timeline = self.oauth_req('https://api.twitter.com/1.1/statuses/home_timeline.json')
        print(home_timeline)
        assert home_timeline is not None

    def test_post_timeline(self):
        status = "Test Status {}".format(self.make_random_string(6))
        payload = "status={}".format(urllib.parse.quote(status))
        response = self.oauth_req('https://api.twitter.com/1.1/statuses/update.json', http_method="POST", post_body=payload)
        print(response)
        assert response is not None
        assert status in str(response)

    def oauth_req(self, url, http_method="GET", post_body="", http_headers=None):
        consumer = oauth2.Consumer(key=self.CONSUMER_KEY, secret=self.CONSUMER_SECRET)
        token = oauth2.Token(key=self.ACCESS_TOKEN, secret=self.ACCESS_TOKEN_SECRET)
        client = oauth2.Client(consumer, token)
        resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
        return content

    def make_random_string(self, num_chars):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(num_chars))

