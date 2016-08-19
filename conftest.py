import logging
from logging import handlers

from os import path

from Config import Config

MAX_LOG_SIZE = 999999

_config = None
_config_file_name = None


def pytest_addoption(parser):
    parser.addoption("--config", action="store", default='local',
                     help="specify the config file to use for tests")


def pytest_configure(config):
    get_config(config)
    setup_logging()


def setup_logging():
    log_file_path = path.join(_config.current_dir, _config.logging_path, _config.LOG_FILE_NAME)
    # create logger with logger id in Config
    logger = logging.getLogger(Config.LOGGER_ID)
    logger.setLevel(_config.logging_level)
    # create file handler which logs even debug messages
    fh = logging.handlers.RotatingFileHandler(log_file_path, maxBytes=50000, backupCount=5)
    fh.setLevel(_config.logging_level)
    fh.doRollover()
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(_config.logging_level)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    print()
    logger.info("TheTestFramework Tests starting...")

def get_config(pytest_config):
    global _config, _config_file_name
    if _config is None:
        _config_file_name = pytest_config.getoption('config')
        print("\nconfig file is {}".format(_config_file_name))
        _config = Config(_config_file_name)
        _config.read_config()
    return _config