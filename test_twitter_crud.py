import logging
import pytest

import conftest
from Config import Config
from DataObjects.PostStatusRequest import PostStatusRequest
from DataObjects.PostStatusResponse import PostStatusResponse
from Helpers.CredsContainer import CredsContainer
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
                                                      self.config.twitter_auth_creds,
                                                      Config.LOGGER_ID)
        self.logger.info("")
        self.logger.info("Running TestTwitterCRUD Tests")

    def teardown_class(self):
        self.logger.info("")
        self.logger.info("Teardown: Remove all but 2 tweets")
        # I have found occasionally that instantiated classes inside of tests lose their sense of "self".
        # It's happened here.  No idea why.
        teardown_response_record = self.get_timeline(self)
        for x in range(0, len(teardown_response_record.status_list) - 2):
            self.delete_status_from_timeline(self, teardown_response_record.status_list[x].id, ignore_status=True)

    def test_get_timeline(self):
        self.logger.info("")
        self.logger.info("Get timeline test")
        # Post something to the timeline to find later
        post_response_record_text = self.post_to_timeline().text

        response_record = self.get_timeline()
        assert len(response_record.status_list) > 0
        assert response_record.find_record_with_status_text(post_response_record_text), \
            "Could not find record with posted text in timeline"

    def test_post_to_timeline(self):
        tweet_text = "Test Post to timeline: {}".format(TestHelpers.make_random_string(6))
        self.logger.info("")
        self.logger.info("Post to timeline test")
        response_record = self.post_to_timeline(tweet_text)
        assert response_record.text == tweet_text

        # Retrieve timeline, and verify our post is in there
        response_record = self.get_timeline()
        assert response_record.find_record_with_status_text(tweet_text), \
            "Could not find record with posted text in timeline"

    def test_delete_from_timeline(self):
        # Post a status so we can delete it.
        post_tweet_response = self.post_to_timeline()
        assert post_tweet_response.id is not None

        # delete record
        deleted_response = self.delete_status_from_timeline(post_tweet_response.id)
        assert deleted_response.id == post_tweet_response.id

        # get timeline and make sure deleted tweet is gone
        timeline_response = self.get_timeline()
        assert timeline_response.find_record_by_id(deleted_response.id) is None

    def test_cannot_get_timeline_with_invalid_consumer_key(self):
        creds = CredsContainer(self.config.twitter_auth_creds.consumer_key,
                               "Bar",
                               self.config.twitter_auth_creds.access_token,
                               self.config.twitter_auth_creds.access_token_secret)
        bad_twitter_service = TwitterStatusesService(self.config.twitter_api_base_url,
                                                     creds, Config.LOGGER_ID)
        response = bad_twitter_service.get_home_timeline()
        TestHelpers.verify_http_response(response, 401, "Get timeline with invalid consumer key", True)

    def test_cannot_get_timeline_with_invalid_access_token(self):
        creds = CredsContainer(self.config.twitter_auth_creds.consumer_key,
                               self.config.twitter_auth_creds.access_token_secret,
                               self.config.twitter_auth_creds.access_token,
                               "Bar")
        bad_twitter_service = TwitterStatusesService(self.config.twitter_api_base_url,
                                                     creds, Config.LOGGER_ID)
        response = bad_twitter_service.get_home_timeline()
        TestHelpers.verify_http_response(response, 401, "Get timeline with invalid consumer key", True)

    def test_cannot_delete_tweet_that_has_been_deleted(self):
        # Post a status so we can delete it.
        post_tweet_response = self.post_to_timeline()
        assert post_tweet_response.id is not None

        # delete record
        deleted_response = self.delete_status_from_timeline(post_tweet_response.id)
        assert deleted_response.id == post_tweet_response.id

        # delete record again
        response = self.twitter_service.delete_status(post_tweet_response.id)
        TestHelpers.verify_http_response(response, 404, "delete tweet that has already been deleted", True)

    def test_cannot_post_status_without_status_text(self):
        tweet_text = ""
        self.logger.info("")
        self.logger.info("Cannot post status without status text")
        payload = PostStatusRequest(tweet_text)
        response = self.twitter_service.post_tweet(payload.create_query_string())
        TestHelpers.verify_http_response(response, 403, "Cannot post status without status text")

    def test_sql_injection_in_status(self):
        # Wee need to make our tweet unique.
        tweet_text = "select * from users --{}".format(TestHelpers.make_random_string(6))
        self.logger.info("")
        self.logger.info("test sql inject in status")
        response_record = self.post_to_timeline(tweet_text)
        assert response_record.text == tweet_text

        # Retrieve timeline, and verify our post is in there
        response_record = self.get_timeline()
        assert response_record.find_record_with_status_text(tweet_text), \
            "Could not find record with posted text in timeline"

    def get_timeline(self):
        response = self.twitter_service.get_home_timeline()
        TestHelpers.verify_http_response(response, 200, "Get Twitter Account Timeline")
        response_record = PostStatusResponse.list_from_dict(response.response_json)
        return response_record

    def post_to_timeline(self, tweet_text=None):
        # This will add a status to the timeline
        if tweet_text is None:
            tweet_text = "Test Status {}".format(TestHelpers.make_random_string(6))
        payload = PostStatusRequest(tweet_text)
        self.logger.debug("Post status payload = {}".format(payload.create_query_string()))
        response = self.twitter_service.post_tweet(payload.create_query_string())
        TestHelpers.verify_http_response(response, 200, "Post to Timeline")
        response_record = PostStatusResponse.from_dict(response.response_json)
        return response_record

    def delete_status_from_timeline(self, status_id, ignore_status=False):
        response = self.twitter_service.delete_status(status_id)
        if ignore_status is False:
            TestHelpers.verify_http_response(response, 200, "Delete Status from timeline")
        else:
            # if we did ignore status, do not parse the response.
            return None
        response_record = PostStatusResponse.from_dict(response.response_json)
        return response_record
