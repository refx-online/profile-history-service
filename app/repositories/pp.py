from __future__ import annotations

from typing import Any

from app.common.context import Context


class PPRepo:
    READ_PARAMS = """\
        `user_id`, `mode`, `captured_at`, `pp`
    """

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def fetch_many(
        self,
        user_id: int,
        mode: int,
        limit: int = 89,
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
