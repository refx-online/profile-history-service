from __future__ import annotations

from typing import Any

from app.common.context import Context


class RanksRepo:
    READ_PARAMS = """\
        `user_id`, `mode`, `captured_at`, `rank`, `country_rank` AS `c_rank`
    """

    READ_PEAK_PARAMS = """\
        `user_id`, `mode`, `captured_at`, `rank`
    """

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def fetch_peak(
        self,
        user_id: int,
        mode: int,
    ) -> dict[str, Any] | None:
        query = f"""\
            SELECT {self.READ_PEAK_PARAMS} FROM `user_profile_history`
                WHERE `user_id` = :user_id AND `mode` = :mode AND `rank` > 0
                ORDER BY `rank`, `captured_at` ASC LIMIT 1
        """
        params = {
            "user_id": user_id,
            "mode": mode,
        }
        return await self.ctx.db.fetch_one(query, params)

    async def fetch_many(
        self,
        user_id: int,
        mode: int,
        limit: int = 89,  # one will be added in api.
    ) -> list[dict[str, Any]]:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM `user_profile_history`
             WHERE `user_id` = :user_id AND `mode` = :mode ORDER BY `captured_at` DESC LIMIT :limit
        """
        params = {
            "user_id": user_id,
            "mode": mode,
            "limit": limit,
        }
        return await self.ctx.db.fetch_all(query, params)
