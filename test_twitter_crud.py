import random
import string
import urllib
from urllib.parse import urlencode

import pytest

from Config import Config
from WebServicesClients.TwitterStatusesService import TwitterStatusesService


class TestTwitterCRUD:
    config_file_name = None
    config = None
    twitter_service = None

    def setup_class(self):
        self.config_file_name = pytest.config.getoption('config')
        print("\nconfig file is {}".format(self.config_file_name))
        self.config = Config(self.config_file_name)
        self.config.read_config()
        self.twitter_service = TwitterStatusesService(self.config.twitter_api_base_url,
                                                      self.config.consumer_key,
                                                      self.config.consumer_secret,
                                                      self.config.access_token,
                                                      self.config.access_token_secret)

    def test_get_timeline(self):
        response = self.twitter_service.get_home_timeline()
        assert response.response_code == '200'
        assert response.response_json is not None
        print(response.response_json)

    def test_post_timeline(self):
        status = "Test Status {}".format(self.make_random_string(6))
        payload = "status={}".format(urllib.parse.quote(status))
        response = self.twitter_service.post_tweet(payload)
        assert response.response_code == '200'
        assert response.response_json is not None
        print(response.response_json)
        assert status in str(response.response_json)

    def make_random_string(self, num_chars):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(num_chars))

