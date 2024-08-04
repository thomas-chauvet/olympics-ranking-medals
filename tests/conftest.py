import pytest

from src.config.config import settings


@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    """Set test settings for all tests.

    This fixture is automatically used by all tests.

    [source](https://www.dynaconf.com/advanced/#a-python-program)
    """
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing")
