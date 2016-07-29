import random
import string
import urllib
from urllib.parse import urlencode

import oauth2
import pytest

from Config import Config


class TestTwitterCRUD:
    config_file_name = None
    config = None

    def setup_class(self):
        self.config_file_name = pytest.config.getoption('config')
        print("\nconfig file is {}".format(self.config_file_name))
        self.config = Config(self.config_file_name)
        self.config.read_config()

    def test_get_timeline(self):
        home_timeline = self.oauth_req('{}/1.1/statuses/home_timeline.json'.format(self.config.twitter_api_base_url))
        print(home_timeline)
        assert home_timeline is not None

    def test_post_timeline(self):
        status = "Test Status {}".format(self.make_random_string(6))
        payload = "status={}".format(urllib.parse.quote(status))
        response = self.oauth_req('{}/1.1/statuses/update.json'.format(self.config.twitter_api_base_url),
                                  http_method="POST", post_body=payload)
        print(response)
        assert response is not None
        assert status in str(response)

    def oauth_req(self, url, http_method="GET", post_body="", http_headers=None):
        consumer = oauth2.Consumer(key=self.config.consumer_key, secret=self.config.consumer_secret)
        token = oauth2.Token(key=self.config.access_token, secret=self.config.access_token_secret)
        client = oauth2.Client(consumer, token)
        resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
        return content

    def make_random_string(self, num_chars):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(num_chars))

