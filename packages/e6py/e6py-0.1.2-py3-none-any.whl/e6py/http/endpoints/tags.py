from typing import Any, List, Optional

from e6py.http.route import Route
from e6py.models import Category
from e6py.models.tag import Tag, TagAlias

VALID_ORDERS = ["date", "count", "name"]
VALID_STATUSES = ["approved", "active", "pending", "deleted", "retired", "processing", "queued"]
VALID_ALIAS_ORDERS = ["status", "created_at", "updated_at", "name", "tag_count"]


class TagRequests:
    request: Any

    def _validate_category(self, category) -> None:
        if category:
            if isinstance(category, Category):
                category = category.value
            elif isinstance(category, int):
                if category not in Category:
                    raise ValueError(f"Invalid category: {category}")
            elif isinstance(category, str):
                if category not in Category:
                    raise ValueError(f"Invalid category: {category}")
                category = Category[category].value
            else:
                raise ValueError(f"Invalid category: {category}")

    def get_tags(
        self,
        name_matches: str = None,
        category: Category | int | str = None,
        order: str = None,
        hide_empty: bool = None,
        has_wiki: Optional[bool] = None,
        has_artist: Optional[bool] = None,
        page: int = None,
        before: int = None,
        after: int = None,
        limit: int = 75,
    ) -> List[Tag] | None:
        """
        Get tags with specified arguments

        Args:
            name_matches: Name expression to match against, use `*` for wildcard
            category: Category to search for
            hide_empty: Hide empty tags
            has_wiki: Show tags with or without a wiki, blank for both
            has_artist: Show tags with or without an artist page, blank for both
            page: Page number, max 750
            before:  Get tags before this tag, overrides page
            after: Get tags after this tag, overrides before
            limit: Number of tags to get, max 320

        Returns:
            List of tags if any found

        Raises:
            ValueError: Invalid category
            ValueError: Invalid order
            ValueError: Too high of limit
        """
        if order and order not in VALID_ORDERS:
            raise ValueError(f"Invalid order {order}, expected one of: {', '.join(VALID_ORDERS)}")

        self._validate_category(category)

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

        data = self.request(
            Route("GET", "/tags.json"),
            search__name_matches=name_matches,
            search__category=category,
            search__order=order,
            search__hide_empty=hide_empty,
            search__has_wiki=has_wiki,
            search__has_artist=has_artist,
            limit=limit,
            page=page,
        )

        tags = Tag.from_list(data, self) if data else None
        if self.cache and tags:
            for tag in tags:
                self._tag_cache[tag.id] = tag
        return tags

    def get_tag(self, tag_id: int) -> Tag | None:
        """
        Get specified tag.

        Args:
            tag_id: ID of tag

        Returns:
            Specified tag if it exists
        """
        if self.cache and (tag := self._tag_cache.get(tag_id)):
            return tag
        data = self.request(Route("GET", f"/tags/{tag_id}.json"))
        tag = Tag.from_dict(data, self) if data else None
        if self.cache:
            self._tag_cache[tag_id] = tag
        return tag

    def get_tag_aliases(
        self,
        name_matches: str = None,
        status: str = None,
        order: str = None,
        from_category: Category | int | str = None,
        to_category: Category | int | str = None,
        page: int = None,
        before: int = None,
        after: int = None,
        limit: int = 75,
    ) -> List[TagAlias] | None:
        """
        Get tag aliases.

        Args:
            name_matches: Name expression to match against, use `*` for wildcard
            status: Status of alias
            order: Sort order
            from_category: Previous tag category
            to_category: New tag category
            page: Page number, max 750
            before:  Get tags before this tag, overrides page
            after: Get tags after this tag, overrides before
            limit: Number of tags to get, max 320

        Returns:
            List of tag aliases if they exist

        Raises:
            ValueError: Invalid status
            ValueError: Invalid order
            ValueError: Invalid category
            ValueError: Too many pages
            ValueError: Too high of limit
        """
        if status and status not in VALID_STATUSES:
            raise ValueError(f"Invalid status {status}, expected one of: {', '.join(VALID_STATUSES)}")

        if order and order not in VALID_ALIAS_ORDERS:
            raise ValueError(f"Invalid order {order}, expected one of: {', '.join(VALID_ALIAS_ORDERS)}")

        self._validate_category(from_category)
        self._validate_category(to_category)

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

        data = self.request(
            Route("GET", "/tag_aliases.json"),
            search__name_matches=name_matches,
            search__status=status,
            search__order=order,
            search__antecedent_tag__category=from_category,
            search__consequent_tag__category=to_category,
            limit=limit,
            page=page,
        )
        aliases = TagAlias.from_list(data, self) if data else None
        if self.cache and aliases:
            for alias in aliases:
                self._alias_cache[alias.id] = alias

        return aliases

    def get_tag_alias(self, alias_id: int) -> TagAlias | None:
        """
        Get specific tag alias

        Args:
            alias_id: Tag alias ID

        Returns:
            Tag alias if it exists
        """
        if self.cache and (alias := self._alias_cache.get(alias_id)):
            return alias
        data = self.request(Route("GET", f"/tag_aliases/{alias_id}.json"))
        alias = TagAlias.from_dict(data, self) if data else None
        if self.cache:
            self._alias_cache[alias_id] = alias
        return alias
