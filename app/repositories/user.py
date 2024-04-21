from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.common.context import Context

mode_map = {
    0: ("users_stats", "std"),
    1: ("users_stats", "taiko"),
    2: ("users_stats", "ctb"),
    3: ("users_stats", "mania"),
    4: ("rx_stats", "std"),
    5: ("rx_stats", "taiko"),
    6: ("rx_stats", "ctb"),
    8: ("ap_stats", "std"),
}


class UsersRepo:
    READ_PARAMS = """\
        `u`.`privileges`, `st`.`country`, `s`.`latest_pp_awarded_{}` AS `latest_pp_awarded`
    """

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def fetch_one(
        self,
        user_id: int,
        mode: int,
    ) -> Mapping[str, Any] | None:
        (db_table, mode_name) = mode_map[mode]
        read_params = self.READ_PARAMS.format(mode_name)

        query = f"""\
            SELECT {read_params}
              FROM `users` `u` INNER JOIN `{db_table}` `s` INNER JOIN `users_stats` `st` ON `st`.`id` = `s`.`id` ON `u`.`id` = `s`.`id`
             WHERE `u`.`id` = :user_id LIMIT 1
        """
        params = {
            "user_id": user_id,
        }
        return await self.ctx.db.fetch_one(query, params)
