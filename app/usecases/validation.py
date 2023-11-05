from __future__ import annotations

import time


def is_restricted(privileges: int) -> bool:
    return privileges & 1 == 0


def is_not_active(latest_pp_awarded: int) -> bool:
    delta_time = int(time.time()) - latest_pp_awarded
    days = delta_time / 60 / 60 / 24
    return days > 60
