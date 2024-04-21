#!/usr/bin/env python3.10
# To run it you need to:
# `cd path/to/profile-history-service && python -m app.workers.cronjobs.crawler`
from __future__ import annotations

import asyncio
import datetime
import time
from collections.abc import Mapping
from typing import Any

import aioredis

from app.common import settings
from app.services import database

redis_map = {
    0: ("leaderboard", "std"),
    1: ("leaderboard", "taiko"),
    2: ("leaderboard", "ctb"),
    3: ("leaderboard", "mania"),
    4: ("relaxboard", "std"),
    5: ("relaxboard", "taiko"),
    6: ("relaxboard", "ctb"),
    8: ("autoboard", "std"),
}


async def fetch_rank(
    user_id: int,
    mode: int,
) -> int:
    (redis_key, mode_name) = redis_map[mode]
    current_rank = await redis.zrevrank(f"ripple:{redis_key}:{mode_name}", user_id)

    if current_rank is None:
        current_rank = 0
    else:
        current_rank += 1

    return current_rank


async def fetch_c_rank(
    user_id: int,
    mode: int,
    country: str,
) -> int:
    (redis_key, mode_name) = redis_map[mode]
    current_rank = await redis.zrevrank(
        f"ripple:{redis_key}:{mode_name}:{country.lower()}",
        user_id,
    )

    if current_rank is None:
        current_rank = 0
    else:
        current_rank += 1

    return current_rank


async def fetch_pp(
    user_id: int,
    mode: int,
) -> int:
    params = {
        "user_id": user_id,
        "mode": mode,
    }
    current_pp = await db.fetch_val(
        """
        SELECT `pp`
        FROM `user_stats`
        WHERE `user_id` = :user_id
        AND `mode` = :mode
        """,
        params,
    )

    if current_pp is None:
        current_pp = 0

    return current_pp


async def gather_profile_history(user: Mapping[str, Any]) -> None:
    user_id = user["id"]
    privileges = user["privileges"]

    start_time = int(time.time())

    for mode in (0, 1, 2, 3, 4, 5, 6, 8):
        latest_pp_awarded = await db.fetch_val(
            """
            SELECT `latest_pp_awarded`
            FROM `user_stats`
            WHERE `user_id` = :user_id
            AND `mode` = :mode
            """,
            {"user_id": user_id, "mode": mode},
        )
        inactive_days = (start_time - latest_pp_awarded) / 60 / 60 / 24

        if inactive_days > 60 or not privileges & 1:
            ranks = await db.fetch_one(
                """
                SELECT `rank`, `country_rank`
                FROM `user_profile_history`
                WHERE `user_id` = :user_id
                AND `mode` = :mode
                ORDER BY `captured_at` DESC
                """,
                {"user_id": user_id, "mode": mode},
            )
            if not ranks:
                continue
            user_rank = ranks["rank"]
            country_rank = ranks["country_rank"]
        else:
            user_rank = await fetch_rank(user_id, mode)
            country_rank = await fetch_c_rank(user_id, mode, user["country"])

        pp_val = await fetch_pp(user_id, mode)
        captured_at = datetime.datetime.now()

        if not user_rank and not pp_val:
            continue

        await db.execute(
            """
            INSERT INTO `user_profile_history`
            (`user_id`, `mode`, `pp`, `rank`, `country_rank`, `captured_at`)
            VALUES (:user_id, :mode, :pp, :rank, :c_rank, :captured_at)
            """,
            {
                "user_id": user_id,
                "mode": mode,
                "pp": pp_val,
                "rank": user_rank,
                "c_rank": country_rank,
                "captured_at": captured_at,
            },
        )


async def async_main() -> int:
    global redis, db

    redis = await aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    )
    db = database.Database(
        read_dsn="mysql+asyncmy://{username}:{password}@{host}:{port}/{db}".format(
            username=settings.READ_DB_USER,
            password=settings.READ_DB_PASS,
            host=settings.READ_DB_HOST,
            port=settings.READ_DB_PORT,
            db=settings.READ_DB_NAME,
        ),
        write_dsn="mysql+asyncmy://{username}:{password}@{host}:{port}/{db}".format(
            username=settings.WRITE_DB_USER,
            password=settings.WRITE_DB_PASS,
            host=settings.WRITE_DB_HOST,
            port=settings.WRITE_DB_PORT,
            db=settings.WRITE_DB_NAME,
        ),
    )
    await db.connect()

    users = await db.fetch_all(
        """
        SELECT `id`, `privileges`, `country`
        FROM `users`
        """,
    )
    await asyncio.gather(*[gather_profile_history(user) for user in users])

    await db.disconnect()
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(async_main())
    raise SystemExit(exit_code)
