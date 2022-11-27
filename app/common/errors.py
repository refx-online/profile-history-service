from __future__ import annotations

from enum import Enum


class ServiceError(str, Enum):
    USERS_NOT_FOUND = "users.not_found"
    USERS_IS_RESTRICTED = "users.is_restricted"
    USERS_IS_NOT_ACTIVE = "users.is_not_active"
    RANKS_NOT_FOUND = "ranks.not_found"
    PP_NOT_FOUND = "pp.not_found"
