from __future__ import annotations

from typing import Any
from typing import Mapping

from pydantic import BaseModel


class UserInfo(BaseModel):
    privileges: int
    country: str
    latest_pp_awarded: int

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> UserInfo:
        return cls(
            privileges=mapping["privileges"],
            country=mapping["country"],
            latest_pp_awarded=mapping["latest_pp_awarded"],
        )
