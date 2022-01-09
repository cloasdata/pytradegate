import datetime
import pathlib
import hashlib
import typing
import os
import pickle
import functools

import requests
from requests import Response

class Request:
    def __init__(self, header: dict):
        self._header = header
        self._response = None

    @property
    def header(self):
        return self._header

    @property
    def response(self) -> typing.Optional[Response]:
        return self._response

    def __call__(self, url: str) -> Response:
        return self.request(url)

    def request(self, url: str) -> Response:
        """
        Simple downloader which uses requests get method.
        raises http error

        :param url: An url to any website. The hash of the url is used as key for the cache.
        :return: tuple(response, status)
        """
        self._response = requests.get(
            url=url,
            headers=self._header.pop("headers", None),
            proxies=self._header.pop("proxies", None),
            timeout=self._header.pop("timeout", None)
        )
        if self._response.status_code >= 400:
            raise requests.exceptions.HTTPError(self._response.status_code)
        else:
            return self._response


class CachedRequest(Request):
    """
    Wraps requests get method. If cache is configured class tries to query the cache. If no response is found
    it fires the http get
    The cache is highly recommended to avoid any abusing.
    """

    def __init__(self, header: dict, path: str, validity: int):
        super().__init__(header)
        self._validity = validity
        self._path = path
        self._header = header if header else dict()

    @property
    def path(self):
        return self._path

    def _load_cache(self, url: str) -> tuple[typing.Optional[datetime.datetime], typing.Optional[requests.Response]]:
        url_hash = hashlib.md5(url.encode()).hexdigest()
        path = pathlib.Path(self._path) / url_hash[:2] / url_hash[2:]
        if os.path.exists(path):
            with open(path, "rb") as pickle_file:
                return pickle.load(pickle_file)
        else:
            return None, None

    def _dump_cache(self, url: str, response: requests.Response):
        url_hash = hashlib.md5(url.encode()).hexdigest()
        path = pathlib.Path(self._path) / url_hash[:2]
        if not os.path.exists(path):
            os.makedirs(path)
        file = path / url_hash[2:]
        timestamp = datetime.datetime.today()
        obj = (timestamp, response)
        with open(file, "xb") as pickle_file:
            pickle.dump(obj, pickle_file)

    def request(self, url: str) -> Response:
        """
        Simple downloader which uses requests get method.
        raises http error

        :param url: An url to any website. The hash of the url is used as key for the cache.
        :return: tuple(response, status)
        """
        get = functools.partial(super(CachedRequest, self).request, url)

        timestamp, response = self._load_cache(url)
        today = datetime.datetime.today()
        valid = datetime.timedelta(days=self._validity)
        if not response or (today - timestamp > valid):
            response = get()
            self._dump_cache(url, response)
        return response
