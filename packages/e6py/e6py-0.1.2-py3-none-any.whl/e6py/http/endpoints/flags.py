from typing import Any, List

from e6py.http.route import Route
from e6py.models.flag import Flag
from e6py.models.tag import Tag

VALID_CATEGORIES = ["normal", "unapproved", "deleted", "banned", "duplicate"]


class FlagRequests:
    request: Any

    def get_flags(
        self,
        is_resolved: bool = None,
        category: str = None,
        reason: str = None,
        post_id: int = None,
        creator_id: int = None,
        creator_name: int = None,
        post_tags_match: Tag | str | List[str | Tag] = None,
        page: int = None,
        before: int = None,
        after: int = None,
        limit: int = 75,
    ) -> List[Flag] | None:
        """
        Get flags with specified arguments

        Args:
            resolved: Limit search to resolved/not resolved/any
            category: Category, one of: normal, unapproved, deleted, banned, duplicate
            reason: Flag reason, use `*` for wildcard
            post_id: Post to get flags of
            creator_id: ID of creator
            creator_name: Name of creator
            post_tags_match: List of tags to limit search to
            page: Page number, max 750
            before:  Get flags before this flag, overrides page
            after: Get flags after this flag, overrides before
            limit: Number of flags to get, max 320

        Returns:
            List of flags if any found

        Raises:
            ValueError: Invalid category
            ValueError: Too high of limit
        """
        if category and category not in VALID_CATEGORIES:
            raise ValueError(f"Invalid category {category}, expected one of: {', '.join(VALID_CATEGORIES)}")

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

        if post_tags_match and isinstance(post_tags_match, list):
            post_tags_match = "+".join([tag.name if isinstance(tag, Tag) else tag for tag in post_tags_match])
        elif post_tags_match and isinstance(post_tags_match, Tag):
            post_tags_match = post_tags_match.name
        elif post_tags_match and isinstance(post_tags_match, str):
            post_tags_match = post_tags_match.replace(" ", "+")

        data = self.request(
            Route("GET", "/post_flags.json"),
            search__is_resolved=is_resolved,
            search__category=category,
            search__reason=reason,
            search__post_id=post_id,
            search__creator_id=creator_id,
            search__creator_name=creator_name,
            search__post_tags_match=post_tags_match,
            page=page,
            limit=limit,
        )

        flags = Flag.from_list(data, self) if data else None
        if self.cache and flags:
            for flag in flags:
                self._flag_cache[flag.id] = flag

        return flags

    def get_flag(self, flag_id: int) -> Flag | None:
        """
        Get specified flag.

        Args:
            flag_id: ID of flag to get

        Returns:
            Specified flag if it exists
        """
        if self.cache and (flag := self._flag_cache.get(flag_id)):
            return flag

        data = self.request(Route("GET", f"/post_flags/{flag_id}.json"))
        flag = Flag.from_dict(data, self) if data else None
        if self.cache:
            self._flag_cache[flag_id] = flag
        return flag
