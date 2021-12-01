import pytest

from src.pytradegate.api import Instrument, Request


@pytest.fixture
def isin():
    return "DE0007664039"

@pytest.fixture
def request_():
    user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    header = {'user-agent': user_agent}
    request = Request(header=header)
    return request

class TestAPI:
    def test_instrument(self, isin, request_):
        # GIVEN
        # isin
        # WHEN user makes new Instrument
        vw = Instrument(isin, request_)
        # THEN data should be available
        ask = vw.ask
        assert ask > 0

    def test_throttle(self, isin, request_):
        # GIVEN
        # isin
        # WHEN user makes new Instrument
        vw = Instrument(isin, request_)
        # AND user queries serveral times
        ask= vw.ask
        first_time = vw._last_query
        for _ in range(10):
            ask = vw.ask
            #THEN ask should remain the same
            assert ask == vw.ask
            # timestamp should be the the same
            assert first_time == vw._last_query

