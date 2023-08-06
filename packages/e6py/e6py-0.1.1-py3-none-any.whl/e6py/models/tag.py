from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

import attr

from e6py.mixins import DictSerializationMixin
from e6py.models import Category
from e6py.utils.converters import convert_timestamp

if TYPE_CHECKING:
    from e6py.client import E621Client  # pragma: no cover


def convert_tags(value):
    if isinstance(value, str):
        return value.split(" ")


@attr.s(slots=True, kw_only=True)
class RelatedTag(DictSerializationMixin):
    name: str = attr.ib()
    score: int = attr.ib()


def convert_related(related_tags: str):
    if related_tags == "[]" or not related_tags:
        return []
    related_tags = related_tags.split(" ")
    retval = []
    for i in range(0, len(related_tags), 2):
        retval.append(RelatedTag(name=related_tags[i], score=int(related_tags[i + 1])))

    return retval


@attr.s(slots=True, kw_only=True)
class Tag(DictSerializationMixin):
    _client: "E621Client" = attr.ib(metadata={"no_export": True})

    id: int = attr.ib()
    name: str = attr.ib()
    post_count: int = attr.ib()
    related_tags: List[RelatedTag] = attr.ib(converter=convert_related)
    related_tags_updated_at: datetime = attr.ib(converter=convert_timestamp)
    category: Category = attr.ib(converter=Category)
    is_locked: bool = attr.ib(default=False)
    created_at: datetime = attr.ib(converter=convert_timestamp)
    updated_at: Optional[datetime] = attr.ib(default=None, converter=convert_timestamp)


@attr.s(slots=True, kw_only=True)
class TagAlias(DictSerializationMixin):
    _client: "E621Client" = attr.ib(metadata={"no_export": True})

    id: int = attr.ib()
    antecedent_name: str = attr.ib()
    reason: str = attr.ib()
    creator_id: int = attr.ib()
    created_at: datetime = attr.ib(converter=convert_timestamp)
    forum_post_id: int = attr.ib()
    updated_at: Optional[datetime] = attr.ib(converter=convert_timestamp)
    forum_topic_id: int = attr.ib()
    consequent_name: str = attr.ib()
    status: str = attr.ib()
    post_count: int = attr.ib()
    approver_id: Optional[int] = attr.ib()
