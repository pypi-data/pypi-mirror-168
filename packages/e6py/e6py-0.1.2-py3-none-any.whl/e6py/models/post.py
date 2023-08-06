import os
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

import attr

from e6py.mixins import DictSerializationMixin
from e6py.utils.converters import convert_timestamp
from e6py.utils.hash import hash_file

if TYPE_CHECKING:
    from e6py.client import E621Client  # pragma: no cover


@attr.s(slots=True, kw_only=True)
class File(DictSerializationMixin):
    width: int = attr.ib()
    height: int = attr.ib()
    ext: str = attr.ib()
    size: int = attr.ib()
    md5: str = attr.ib()
    url: Optional[str] = attr.ib(default=None)

    @ext.validator
    def _ext_check(self, _attribute, value):
        if value not in ["jpg", "png", "gif", "swf", "webm"]:
            raise ValueError("Extension must be one of: jpg, png, gif, swf, webm")


@attr.s(slots=True, kw_only=True)
class Preview(DictSerializationMixin):
    width: int = attr.ib()
    height: int = attr.ib()
    url: Optional[str] = attr.ib(default=None)


@attr.s(slots=True, kw_only=True)
class Sample(DictSerializationMixin):
    has: bool = attr.ib(default=False)
    width: int = attr.ib()
    height: int = attr.ib()
    url: Optional[str] = attr.ib(default=None)
    alternates: dict = attr.ib()


@attr.s(slots=True, kw_only=True)
class Score(DictSerializationMixin):
    up: int = attr.ib()
    down: int = attr.ib()
    total: int = attr.ib()


@attr.s(slots=True, kw_only=True)
class Tags(DictSerializationMixin):
    general: Optional[List[str]] = attr.ib(factory=list)
    species: Optional[List[str]] = attr.ib(factory=list)
    character: Optional[List[str]] = attr.ib(factory=list)
    artist: Optional[List[str]] = attr.ib(factory=list)
    invalid: Optional[List[str]] = attr.ib(factory=list)
    lore: Optional[List[str]] = attr.ib(factory=list)
    meta: Optional[List[str]] = attr.ib(factory=list)
    copyright: Optional[List[str]] = attr.ib(factory=list)


@attr.s(slots=True, kw_only=True)
class Flags(DictSerializationMixin):
    pending: bool = attr.ib(default=True)
    flagged: bool = attr.ib(default=False)
    note_locked: bool = attr.ib(default=False)
    status_locked: bool = attr.ib(default=False)
    rating_locked: bool = attr.ib(default=False)
    deleted: bool = attr.ib(default=False)
    comment_disabled: bool = attr.ib(default=False)


@attr.s(slots=True, kw_only=True)
class Relationship(DictSerializationMixin):
    parent_id: Optional[int] = attr.ib(default=None)
    has_children: bool = attr.ib(default=False)
    has_active_children: bool = attr.ib(default=False)
    children: list = attr.ib(factory=list)


def ensure_cls(cls, lst=False):
    """Validate that the data is an instance of required class"""

    def converter(val):
        if isinstance(val, cls):
            return val
        elif lst and all(isinstance(x, cls) for x in val):
            return val
        else:
            if not lst:
                return cls(**val)
            else:
                data = []
                for item in val:
                    if not isinstance(item, cls):
                        item = cls(**item)
                    data.append(item)
                return data

    return converter


@attr.s(slots=True, kw_only=True)
class Post(DictSerializationMixin):
    _client: "E621Client" = attr.ib(metadata={"no_export": True})

    id: int = attr.ib()
    created_at: datetime = attr.ib(default=datetime.now, converter=convert_timestamp)
    updated_at: Optional[datetime] = attr.ib(default=None, converter=convert_timestamp)
    file: File = attr.ib(converter=ensure_cls(File))
    preview: Preview = attr.ib(converter=ensure_cls(Preview))
    sample: Sample = attr.ib(converter=ensure_cls(Sample))
    score: Score = attr.ib(converter=ensure_cls(Score))
    tags: Tags = attr.ib(converter=ensure_cls(Tags))
    locked_tags: list = attr.ib(factory=list)
    change_seq: int = attr.ib()
    flags: Flags = attr.ib(converter=ensure_cls(Flags))
    rating: str = attr.ib()
    fav_count: int = attr.ib()
    sources: List[str] = attr.ib(factory=list)
    pools: List[int] = attr.ib(factory=list)
    relationships: Relationship = attr.ib(factory=list, converter=ensure_cls(Relationship))
    approver_id: Optional[int] = attr.ib(default=None)
    uploader_id: int = attr.ib()
    description: str = attr.ib()
    comment_count: int = attr.ib()
    is_favorited: Optional[bool] = attr.ib(default=False)
    has_notes: bool = attr.ib(default=False)
    duration: Optional[int] = attr.ib(default=None)

    _downloaded: bool = attr.ib(default=False)

    def download(self, path: Optional[str] = None) -> Optional[bool]:
        """
        Download the post

        Args:
            path: Path to download to, default `Post.file.md5`.`Post.file.ext`

        Returns:
            If file was downloaded
        """
        if self._downloaded:
            return False
        if not path:
            path = f"{self.file.md5}.{self.file.ext}"
        if os.path.exists(path) and hash_file(path) == self.file.md5:
            self._downloaded = True
            return False
        self._client.download_post(self, path)
        self._downloaded = True
        return True
