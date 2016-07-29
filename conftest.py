def pytest_addoption(parser):
    parser.addoption("--config", action="store", default='local',
                     help="specify the config file to use for tests")
