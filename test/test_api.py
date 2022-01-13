import pytest
from src.pytradegate import Request, Instrument, CachedRequest

isins = ["DE0005439004", "DE0007664039"]


@pytest.fixture(params=isins)
def isin(request):
    return request.param


@pytest.fixture
def req_header():
    user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    return {'user-agent': user_agent}


@pytest.fixture
def request_obj(req_header):
    r = Request(header=req_header)
    return r


class TestAPI:
    def test_instrument(self, isin, request_obj):
        # GIVEN
        # isin
        # WHEN user makes new Instrument
        inst = Instrument(isin, request_obj)
        # THEN data should be available
        ask = inst.ask
        assert isinstance(ask, float)
        assert ask > 0

    def test_data_type(self, isin, request_obj):
        inst = Instrument(isin, request_obj)
        for v in inst.data.values():
            assert isinstance(v, float)

    def test_throttle(self, isin, request_obj):
        # GIVEN
        # isin
        # WHEN user makes new Instrument
        inst = Instrument(isin, request_obj)
        # AND user queries serveral times
        ask = inst.ask
        first_time = inst._last_query
        for _ in range(10):
            ask = inst.ask
            # THEN ask should remain the same
            assert ask == inst.ask
            # timestamp should be the the same
            assert first_time == inst._last_query
