from __future__ import annotations

from app.common.context import Context
from app.common.errors import ServiceError
from app.models.user import UserInfo
from app.repositories.user import UsersRepo

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


async def fetch_one(
    ctx: Context,
    user_id: int,
    mode: int,
) -> UserInfo | ServiceError:
    r_repo = UsersRepo(ctx)
    resp = await r_repo.fetch_one(user_id, mode)

    if resp is None:
        return ServiceError.USERS_NOT_FOUND

    return UserInfo.from_mapping(resp)
