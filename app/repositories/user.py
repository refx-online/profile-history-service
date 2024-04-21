from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.common.context import Context


class UsersRepo:
    READ_PARAMS = """\
        `u`.`privileges`, `u.`.`country`, `s`.`latest_pp_awarded`
    """

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def fetch_one(
        self,
        user_id: int,
        mode: int,
    ) -> Mapping[str, Any] | None:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM `users` `u` INNER JOIN `user_stats` `s` ON `u`.`id` = `s`.`user_id`
             WHERE `u`.`id` = :user_id AND `s`.`mode` = :mode LIMIT 1
        """
        params = {
            "user_id": user_id,
            "mode": mode,
        }
        return await self.ctx.db.fetch_one(query, params)
