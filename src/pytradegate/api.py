import datetime
import typing

from src.pytradegate.request import Request, CachedRequest


class Instrument:
    def __init__(self, isin: str, request: typing.Union[Request, CachedRequest], throttle: int = 10):
        self._isin = isin
        self._request = request
        self._url = "https://www.tradegate.de/refresh.php?isin=" + isin
        self._throttle = datetime.timedelta(seconds=throttle)
        self._last_query = datetime.datetime.min
        self._data: dict[str, float] = {}

    @property
    def _refresh(self):
        if self._last_query + self._throttle <= datetime.datetime.now():
            return True
        else:
            return False

    @property
    def ask(self) -> float:
        self._update()
        return self._data.get("ask")

    @property
    def bid(self) -> float:
        self._update()
        return self._data.get("bid")

    @staticmethod
    def _ptofloat(v) -> float:
        if isinstance(v, str):
            return float(v.replace(",", "."))
        else:
            return v

    @property
    def data(self) -> dict:
        return self._data

    def _update(self):
        if self._refresh:
            self._get()

    def _get(self):
        self._last_query = datetime.datetime.now()
        resp = self._request(self._url)
        json: dict[str, typing.Union[float, str]] = resp.json()
        # sever responding sometimes with string instead of float
        for k, v in json.items():
            self._data[k] = self._ptofloat(v)

    def __repr__(self):
        return f"Instrument(isin={self._isin}, request={self._request}, throttle={self._throttle})"
