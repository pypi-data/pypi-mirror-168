import logging
import time
import traceback
from datetime import datetime
from typing import Any, ClassVar, Dict, Optional

import requests
from requests import Response, Session

import e6py
from e6py.const import MISSING
from e6py.errors import HTTPException, Forbidden, NotFound, E621Error
from e6py.http.endpoints import PostRequests, FlagRequests, NoteRequests, TagRequests, PoolRequests
from e6py.http.route import Route, RawRoute

log = logging.getLogger(__name__)


class HTTPClient(PostRequests, FlagRequests, NoteRequests, TagRequests, PoolRequests):
    BASE: ClassVar[str] = None

    def __init__(self, login: str, api_key: str, cache: bool = True) -> "HTTPClient":
        self.__session = Session()
        self._retries: int = 5
        self.cache = cache
        self.login = login
        self.api_key = api_key
        if not self.login or not self.api_key:
            raise ValueError("Both login and api_key are required")
        self.user_agent = f"e6py/{e6py.__version__} (by zevaryx on e621)"
        self.__last_request = 0

        # Caches
        self._query_cache = dict()  # TODO: Figure out format for keys
        self._alias_cache = dict()
        self._flag_cache = dict()
        self._note_cache = dict()
        self._pool_cache = dict()
        self._post_cache = dict()
        self._tag_cache = dict()

    def __del__(self):
        self.close()

    def _get_cache(self, type: str) -> dict:  # pragma: no cover
        match type:
            case "flag":
                return self._flag_cache
            case "note":
                return self._note_cache
            case "pool":
                return self._pool_cache
            case "post":
                return self._post_cache
            case "tag":
                return self._tag_cache

    def _check_cache(self, func, type: str):  # pragma: no cover
        def checker(func, *args, **kwargs):
            key = f"{type}_id"
            cache = self._get_cache(type)
            if self.cache and (obj := cache.get(key)):
                return obj
            obj = func(*args, **kwargs)
            if self.cache:
                cache[kwargs.get(key)] = obj
            return obj

        return checker

    def close(self) -> None:
        """Close the session"""
        if self.__session:
            self.__session.close()

    def download(self, route: RawRoute, path: str) -> bool:
        """
        Download a file from e621

        Args:
            route: Route to image
        """
        headers: Dict[str, str] = {"User-Agent": self.user_agent}
        auth = None

        if self.login and self.api_key:
            auth = requests.auth.HTTPBasicAuth(self.login, self.api_key)

        with self.__session.request(route.method, route.url, headers=headers, auth=auth, stream=True) as response:
            if response.status_code == 200:
                with open(path, "wb+") as f:
                    f.write(response.content)

        return True

    def request(self, route: Route, data: dict = MISSING, **kwargs: Dict[str, Any]) -> Any:
        """
        Make a request to e621

        Args:
            route: Route to take
            data: Data payload to send in the request
        """
        if self.__last_request > 0:
            time.sleep(max(self.__last_request + 1 - datetime.now().timestamp(), 0))
        headers: Dict[str, str] = {"User-Agent": self.user_agent}
        url = self.BASE + route.url
        auth = None

        if self.login and self.api_key:
            auth = requests.auth.HTTPBasicAuth(self.login, self.api_key)

        if len(kwargs) > 0:
            search_str = []
            for key, value in kwargs.items():
                if value is not None:
                    if "__" in key:
                        sections = key.split("__")
                        key = sections[0]
                        for section in sections[1:]:
                            key += f"[{section}]"
                    search_str.append(f"{key}={value}")
            url += "?" + "&".join(search_str)

        response: Optional[Response] = None
        result: Optional[Dict[str, Any] | str] = None
        self.__last_request = datetime.now().timestamp()
        for tries in range(self._retries):
            try:
                with self.__session.request(route.method, url, headers=headers, auth=auth) as response:
                    result = response.json()
                    if response.status_code == 404:
                        return None
                    if response.status_code in [500, 502]:  # pragma: no cover
                        log.warning(
                            f"{route.method}::{route.url}: Received {response.status_code}, retrying in {1 + tries * 2} seconds"
                        )
                        time.sleep(1 + tries * 2)
                        continue
                    elif response.status_code == 503:  # pragma: no cover
                        log.warning(
                            f"{route.method}::{route.url}: Received {response.status_code}, potential ratelimit, retrying in {1 + tries * 2} seconds"
                        )
                        time.sleep(1 + tries * 2)
                        continue
                    elif not 300 > response.status_code >= 200:  # pragma: no cover
                        self._raise_exception(response, route, result)
                    if "success" in result and result["success"] is False:  # pragma: no cover
                        raise E621Error(f"Request failed: {result['reason']}")
                    if isinstance(result, dict) and len(result) == 1:
                        head_key = list(result.keys())[0]
                        result = result[head_key]
                    return result
            except (Forbidden, NotFound, E621Error, HTTPException):  # pragma: no cover
                raise
            except Exception as e:  # pragma: no cover
                log.error("".join(traceback.format_exception(type(e), e, e.__traceback__)))
                time.sleep(1)

    def _raise_exception(self, response, route, result):  # pragma: no cover
        log.error(f"{route.method}::{route.url}: {response.status_code}")

        if response.status_code == 403:
            raise Forbidden(response, response_data=result, route=route)
        elif response.status_code == 404:
            raise NotFound(response, response_data=result, route=route)
        elif response.status_code >= 500:
            raise E621Error(response, response_data=result, route=route)
        else:
            raise HTTPException(response, response_data=result, route=route)
