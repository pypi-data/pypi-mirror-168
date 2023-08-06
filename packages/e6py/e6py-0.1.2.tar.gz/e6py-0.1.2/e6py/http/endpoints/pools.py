from typing import Any, List

from e6py.http.route import Route
from e6py.models.pool import Pool

VALID_CATEGORIES = ["series", "collection"]
VALID_ORDERS = ["name", "created_at", "updated_at", "post_count"]


class PoolRequests:
    request: Any

    def get_pools(
        self,
        name_matches: str = None,
        id: int | List[int] = None,
        description_matches: str = None,
        creator_name: str = None,
        creator_id: int = None,
        is_active: bool = None,
        is_deleted: bool = None,
        category: str = None,
        order: str = None,
        page: int = None,
        before: int = None,
        after: int = None,
        limit: int = 75,
    ) -> List[Pool] | None:
        """
        Get pools.

        Args:
            name_matches: Search by name, use `*` for wildcard
            id: Pool ID or list of pool IDs to search for
            description_matches: Search by description, use `*` for wildcard
            creator_name: Pool creator name
            creator_id: Pool creator id
            is_active: If the pool is active or hidden
            is_deleted: If the pool is deleted
            category: Series or collection
            order: Sort order
            page: Page number, max 750
            before:  Get flags before this flag, overrides page
            after: Get flags after this flag, overrides before
            limit: Number of flags to get, max 320

        Returns:
            List of pools if any found

        Raises:
            ValueError: Invalid category
            ValueError: Invalid order
            ValueError: Too high of limit
        """
        if category and category not in VALID_CATEGORIES:
            raise ValueError(f"Invalid category {category}, expected one of: {', '.join(VALID_CATEGORIES)}")

        if order and order not in VALID_ORDERS:
            raise ValueError(f"Invalid order {order}, expected one of: {', '.join(VALID_ORDERS)}")

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

        if id:
            id = ",".join(str(x) for x in id)

        data = self.request(
            Route("GET", "/pools.json"),
            search__name_matches=name_matches,
            search__id=id,
            search__description_matches=description_matches,
            search__creator_name=creator_name,
            search__is_active=is_active,
            search__is_deleted=is_deleted,
            search__category=category,
            search__order=order,
            page=page,
            limit=limit,
        )
        pools = Pool.from_list(data, self) if data else None
        if self.cache and pools:
            for pool in pools:
                self._pool_cache[pool.id] = pool

        return pools

    def get_pool(self, pool_id: int) -> Pool | None:
        """
        Get pool.

        Args:
            pool_id: ID of pool

        Returns:
            Pool if it exists
        """
        if self.cache and (pool := self._pool_cache.get(pool_id)):
            return pool
        data = self.request(Route("GET", f"/pools/{pool_id}.json"))
        pool = Pool.from_dict(data, self) if data else None
        if self.cache:
            self._pool_cache[pool_id] = pool
        return pool
