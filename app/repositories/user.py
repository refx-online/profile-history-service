from __future__ import annotations

from typing import Any

from app.common.context import Context


class UsersRepo:
    # Tfsjfojasofjssfjasofosofoasmfomasofoasf
    LATEST_PP_AWARDED = """\
        SELECT UNIX_TIMESTAMP(MAX(play_time)) AS `latest_pp_awarded`
        FROM `scores` 
        WHERE `userid` = :user_id 
        AND `mode` = :mode 
        AND `grade` != 'f'
    """

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def fetch_latest_pp_awarded(
        self,
        user_id: int,
        mode: int,
    ) -> str | None: # wait is it str or int
        params = {
            "user_id": user_id,
            "mode": mode,
        }
        row = await self.ctx.db.fetch_one(self.LATEST_PP_AWARDED, params)
        return row["latest_pp_awarded"] if row else None

    async def fetch_one(
        self,
        user_id: int,
        mode: int,
    ) -> dict[str, Any] | None:
        latest_pp_awarded = await self.fetch_latest_pp_awarded(user_id, mode)

        query = f"""\ 
            SELECT `priv`, `country`
            FROM `users`
            WHERE `id` = :user_id
            LIMIT 1
        """
        params = {
            "user_id": user_id,
            "mode": mode,
        }

        user_data = await self.ctx.db.fetch_one(query, params)
        # TODO: dont do this?
        # this just a shortcut, i dont want to fuck up bpy again
        if user_data:
            user_data["latest_pp_awarded"] = latest_pp_awarded

        return user_data
