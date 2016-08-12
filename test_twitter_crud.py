import logging
import urllib
from urllib.parse import urlencode

import pytest

import conftest
from Config import Config
from WebServicesClients.TwitterStatusesService import TwitterStatusesService
from Helpers import TestHelpers


class TestTwitterCRUD:
    config = None
    logger = None

    twitter_service = None

    def setup_class(self):
        self.config = conftest.get_config(pytest.config)
        self.logger = logging.getLogger(Config.LOGGER_ID)
        self.twitter_service = TwitterStatusesService(self.config.twitter_api_base_url,
                                                      self.config.consumer_key,
                                                      self.config.consumer_secret,
                                                      self.config.access_token,
                                                      self.config.access_token_secret,
                                                      Config.LOGGER_ID)
        print()
        self.logger.info("Running TestTwitterCRUD Tests")

    def test_get_timeline(self):
        self.logger.info("Get timeline test")
        response = self.twitter_service.get_home_timeline()
        TestHelpers.verify_http_response(response, 200, "Get Twitter Account Timeline")

    def test_post_to_timeline(self):
        self.logger.info("Post to timeline test")
        status = "Test Status {}".format(TestHelpers.make_random_string(6))
        payload = "status={}".format(urllib.parse.quote(status))
        response = self.twitter_service.post_tweet(payload)
        TestHelpers.verify_http_response(response, 200, "Post to Timeline")
        assert status in str(response.response_json)
