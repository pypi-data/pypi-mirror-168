from typing import Any

import requests

from e6py.const import MISSING


class ClientException(Exception):
    pass


class HTTPException(ClientException):
    """A HTTP request resulted in an exception

    Attributes:
        response aiohttp.ClientResponse: The response of the HTTP request
        text str: The text of the exception, could be None
        status int: The HTTP status code
        code int: The discord error code, if one is provided
        route Route: The HTTP route that was used
    """

    def __init__(self, response: requests.Response, text=MISSING, e621_code=MISSING, **kwargs):
        self.response: requests.Response = response
        self.status: int = response.status_code
        self.code: int = e621_code
        self.text: str = text
        self.errors: Any = MISSING
        self.route = kwargs.get("route", MISSING)

        if data := kwargs.get("response_data"):
            if isinstance(data, dict):
                self.text = data.get("message", MISSING)
                self.code = data.get("code", MISSING)
                self.errors = data.get("errors", MISSING)
            else:
                self.text = data

        super().__init__(f"{self.status}|{self.response.reason}: {f'({self.code}) ' if self.code else ''}{self.text}")


class E621Error(HTTPException):
    pass


class BadRequest(HTTPException):
    pass


class Forbidden(HTTPException):
    pass


class NotFound(HTTPException):
    pass
