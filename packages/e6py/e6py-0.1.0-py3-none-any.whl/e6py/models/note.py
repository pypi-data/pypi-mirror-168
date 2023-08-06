from datetime import datetime
from typing import Optional, TYPE_CHECKING

import attr

from e6py.mixins import DictSerializationMixin
from e6py.utils.converters import convert_timestamp

if TYPE_CHECKING:
    from e6py.client import E621Client  # pragma: no cover


@attr.s(slots=True, kw_only=True)
class Note(DictSerializationMixin):
    _client: "E621Client" = attr.ib(metadata={"no_export": True})

    id: int = attr.ib()
    created_at: datetime = attr.ib(converter=convert_timestamp)
    updated_at: Optional[datetime] = attr.ib(default=None, converter=convert_timestamp)
    creator_id: Optional[int] = attr.ib(default=None)
    x: int = attr.ib()
    y: int = attr.ib()
    width: int = attr.ib()
    height: int = attr.ib()
    version: int = attr.ib()
    is_active: bool = attr.ib(default=True)
    post_id: int = attr.ib()
    body: str = attr.ib()
    creator_name: str = attr.ib()
