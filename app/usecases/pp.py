from __future__ import annotations

import datetime

from app.common.context import Context
from app.models.pp import PPCapture
from app.models.pp import PPHistory
from app.repositories.pp import PPRepo


async def fetch_many(
    ctx: Context,
    user_id: int,
    mode: int,
    limit: int = 89,  # one will be added in api.
) -> PPHistory:
    r_repo = PPRepo(ctx)
    resp = await r_repo.fetch_many(user_id, mode, limit)

    resp = resp[::-1]  # swap it so its in right order.

    data_structure = {"user_id": user_id, "mode": mode, "captures": resp}

    return PPHistory.from_mapping(data_structure)


async def fetch_current(
    ctx: Context,
    user_id: int,
    mode: int,
) -> PPCapture | None:
    params = {
        "id": user_id,
        "mode": mode,
    }
    current_pp = await ctx.db.fetch_val(
        """
        SELECT `pp`
        FROM `stats`
        WHERE `id` = :id
        AND `mode` = :mode
        """,
        params,
    )

    if not current_pp:
        return None

    current_pp_captured_at = datetime.datetime.now()
    data_structure = {"captured_at": current_pp_captured_at, "pp": current_pp}

    return PPCapture.from_mapping(data_structure)
