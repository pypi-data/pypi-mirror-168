from typing import Any, List

from e6py.http.route import RawRoute, Route
from e6py.models.post import Post
from e6py.models.tag import Tag

VALID_STATUS = ["active", "any", "deleted", "flagged", "modqueue", "pending", "unmoderated"]


class PostRequests:
    request: Any
    download: Any

    def get_post(self, post_id: int) -> Post | None:
        """
        Get a specific post.

        Args:
            post_id: ID of post to get

        Returns:
            Specified post if it exists
        """
        if self.cache and (post := self._post_cache.get(post_id)):
            return post
        data = self.request(Route("GET", f"/posts/{post_id}.json"))
        post = Post.from_dict(data, self) if data else None
        if self.cache:
            self._post_cache[post_id] = post
        return post

    def get_posts(
        self,
        status: str = "active",
        page: int = None,
        before: int = None,
        after: int = None,
        limit: int = 75,
        tags: Tag | str | List[str | Tag] = None,
        **kwargs,
    ) -> List[Post] | None:
        """
        Gets posts with specified arguments

        Args:
            status: Post status, one of: active, any, deleted, flagged, modqueue, pending, unmoderated
            page: Page number, max 750
            before: Get posts before this post, overrides page
            after: Get posts after this post, overrides before
            limit: Number of posts to retrieve, max 320
            tags: List of tags to limit search to

        Returns:
            List of posts if any found

        Raises:
            ValueError: Invalid status
            ValueError: Too high of limit
            ValueError: Too high of page
        """
        if status not in VALID_STATUS:
            raise ValueError(f"Invalid status {status}, expected one of: {', '.join(VALID_STATUS)}")

        if before:
            page = f"b{before}"
        elif after:
            page = f"a{after}"
        elif not page:
            page = 0
        elif page > 750:
            raise ValueError("Page must be < 750, consider using 'before'")
        if limit > 320:
            raise ValueError("Limit must be <= 320")

        if tags and isinstance(tags, list):
            tags = "+".join([tag.name if isinstance(tag, Tag) else tag for tag in tags])
        elif tags and isinstance(tags, Tag):
            tags = tags.name
        elif tags and isinstance(tags, str):
            tags = tags.replace(" ", "+")

        data = self.request(Route("GET", "/posts.json"), status=status, page=page, limit=limit, tags=tags, **kwargs)
        posts = Post.from_list(data, self) if data else None
        if self.cache and posts:
            for post in posts:
                self._post_cache[post.id] = post

        return posts

    def download_post(self, post: Post, path: str) -> bool:
        """
        Download a passed-in post

        Args:
            post: Post to download
            path: Target path
        """
        url = post.file.url
        return self.download(RawRoute("GET", url), path)
