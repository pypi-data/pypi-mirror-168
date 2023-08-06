import logging
from typing import ClassVar

from e6py.http.client import HTTPClient

log = logging.getLogger(__name__)


class E621Client(HTTPClient):
    """E621 API Client"""

    BASE: ClassVar[str] = "https://e621.net"


class E926Client(HTTPClient):
    """E926 API Client"""

    BASE: ClassVar[str] = "https://e926.net"
