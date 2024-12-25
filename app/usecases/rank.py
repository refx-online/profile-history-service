from __future__ import annotations

import datetime

from app.common.context import Context
from app.common.errors import ServiceError
from app.models.rank import RankCapture
from app.models.rank import RankHistory
from app.models.rank import RankPeak
from app.repositories.rank import RanksRepo


async def fetch_peak(
    ctx: Context,
    user_id: int,
    mode: int,
) -> RankPeak | ServiceError:
    r_repo = RanksRepo(ctx)
    resp = await r_repo.fetch_peak(user_id, mode)

    if resp is None:
        return ServiceError.PEAK_RANK_NOT_FOUND

    data_structure = {
        "user_id": user_id,
        "mode": mode,
        "captured_at": resp["captured_at"],
        "rank": resp["rank"],
    }
    return RankPeak.from_mapping(data_structure)


async def fetch_many(
    ctx: Context,
    user_id: int,
    mode: int,
    limit: int = 89,  # one will be added in api.
) -> RankHistory:
    r_repo = RanksRepo(ctx)
    resp = await r_repo.fetch_many(user_id, mode, limit)

    resp = resp[::-1]  # swap it so its in right order.

    data_structure = {
        "user_id": user_id,
        "mode": mode,
        "captures": resp,
    }
    return RankHistory.from_mapping(data_structure)


async def fetch_current(
    ctx: Context,
    user_id: int,
    mode: int,
    country: str,
) -> RankCapture | None:
    current_rank = await ctx.redis.zrevrank(f"bancho:leaderboard:{mode}", user_id)
    current_c_rank = await ctx.redis.zrevrank(
        f"bancho:leaderboard:{mode}:{country.lower()}",
        user_id,
    )

    if current_rank is None or current_c_rank is None:
        return None

    current_rank_captured_at = datetime.datetime.now()
    data_structure = {
        "captured_at": current_rank_captured_at,
        "rank": current_rank + 1,  # 0-indexed.
        "c_rank": current_c_rank + 1,
    }

    return RankCapture.from_mapping(data_structure)


async def fetch_current_rank(
    ctx: Context,
    user_id: int,
    mode: int,
) -> RankPeak | None:
    current_rank = await ctx.redis.zrevrank(f"bancho:leaderboard:{mode}", user_id)
    if current_rank is None:
        return None

    current_rank_captured_at = datetime.datetime.now()
    data_structure = {
        "user_id": user_id,
        "mode": mode,
        "captured_at": current_rank_captured_at,
        "rank": current_rank + 1,  # 0-indexed.
    }

    return RankPeak.from_mapping(data_structure)
