from datetime import datetime
from os import sep
from typing import List, Optional, TYPE_CHECKING

import attr

from e6py.mixins import DictSerializationMixin
from e6py.models.post import Post
from e6py.utils.converters import convert_timestamp

if TYPE_CHECKING:
    from e6py.client import E621Client  # pragma: no cover


@attr.s(slots=True, kw_only=True)
class Pool(DictSerializationMixin):
    _client: "E621Client" = attr.ib(metadata={"no_export": True})

    id: int = attr.ib()
    name: str = attr.ib()
    created_at: datetime = attr.ib(default=datetime.now, converter=convert_timestamp)
    updated_at: Optional[datetime] = attr.ib(default=datetime.now, converter=convert_timestamp)
    creator_id: int = attr.ib()
    description: str = attr.ib()
    is_active: bool = attr.ib(default=True)
    category: str = attr.ib()
    is_deleted: bool = attr.ib(default=False)
    post_ids: List[int] = attr.ib(factory=list)
    creator_name: str = attr.ib()
    post_count: int = attr.ib()

    _posts: List[Post] = attr.ib(factory=list)

    @property
    def posts(self) -> List[Post]:
        """Get all posts in the pool"""
        if not self._posts:
            if self.post_count <= 320:
                self._posts = self._client.get_posts(tags=f"pool:{self.id}", limit=320)
            else:
                for start in self.post_ids[::320]:
                    self._posts += self._client.get_posts(tags=f"pool:{self.id}", limit=320, after=start - 1)
        return self._posts

    def download(self, path: str = None) -> int:
        """
        Download all posts in pool

        Args:
            path: Path to download to, default `Pool.id`

        Returns:
            How many images were downloaded
        """
        if not path:
            path = str(self.id) + sep
        if path[-1] != sep:
            path += sep
        count = 0
        for post in self.posts:
            count += post.download(f"{path}{post.file.md5}.{post.file.ext}")

        return count
