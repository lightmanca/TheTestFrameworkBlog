import configparser
import os

import sys

class Config:
    LOGGER_ID = "API SAMPLE TESTS"
    CONFIG_DIR = 'ConfigFiles'
    COMMON_CONFIG_SECTION = 'common'
    ENV_CONFIG_SECTION = 'env-qa'
    LOG_FILE_NAME = "testlog.log"

    config_file_name = None

    consumer_key = None
    consumer_secret = None
    access_token = None
    access_token_secret = None

    twitter_api_base_url = None

    logging_level = None
    logging_path = None

    logger = None

    # Warning!  The code to set up logging requires this config class.  Do not do any logging in __init__
    def __init__(self, config_file_name):
        try_path = os.path.join(self.current_dir, config_file_name)
        if os.path.exists(try_path):
            self.config_file_name = try_path
        else:
            self.config_file_name = os.path.join(self.current_dir, self.CONFIG_DIR, config_file_name)
        if not os.path.exists(self.config_file_name):
            print("\n\nFatal Error: Config file: {} not found.".format(self.config_file_name))
            sys.exit()

    # Warning!  The code to set up logging requires this config class.  Do not do any logging in read_config
    def read_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file_name)
        self.consumer_key = config[self.COMMON_CONFIG_SECTION]['consumer_key']
        self.consumer_secret = config[self.COMMON_CONFIG_SECTION]['consumer_secret']
        self.access_token = config[self.COMMON_CONFIG_SECTION]['access_token']
        self.access_token_secret = config[self.COMMON_CONFIG_SECTION]['access_token_secret']
        self.logging_level = config[self.COMMON_CONFIG_SECTION]['logging_level']
        self.logging_path = config[self.COMMON_CONFIG_SECTION]['logging_path']

        self.twitter_api_base_url = config[self.ENV_CONFIG_SECTION]['twitter_api_base_url']

        print("Twitter api base url = {}".format(self.twitter_api_base_url))

    @property
    def current_dir(self):
        return os.path.dirname(os.path.abspath(__file__))
