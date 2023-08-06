from datetime import datetime
from typing import Optional, TYPE_CHECKING

import attr

from e6py.mixins import DictSerializationMixin
from e6py.utils.converters import convert_timestamp

if TYPE_CHECKING:
    from e6py.client import E621Client  # pragma: no cover


@attr.s(slots=True, kw_only=True)
class Flag(DictSerializationMixin):
    _client: "E621Client" = attr.ib(metadata={"no_export": True})

    id: int = attr.ib()
    created_at: datetime = attr.ib(converter=convert_timestamp)
    post_id: int = attr.ib()
    reason: str = attr.ib()
    creator_id: Optional[int] = attr.ib(default=None)
    is_resolved: bool = attr.ib(default=False)
    updated_at: Optional[datetime] = attr.ib(default=None, converter=convert_timestamp)
    is_deletion: bool = attr.ib(default=True)
    category: str = attr.ib()
